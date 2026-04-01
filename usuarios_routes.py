from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas import UsuarioSchema, LoginSchema
from models import Usuarios
from utils import gerar_hash, verificar_hash, criar_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

usuario_router = APIRouter(prefix='/usuarios', tags=['usuario'])

@usuario_router.post('/criar_usuarios')
async def criar_usuario(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuarios).filter(Usuarios.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail='esse email já está sendo utilizado')
    usuario = Usuarios(nome=usuario_schema.nome,
                       email=usuario_schema.email,
                       senha=gerar_hash(usuario_schema.senha))
    session.add(usuario)
    session.commit()
    return {
        'message': 'Usuário criado com sucesso'
    }

@usuario_router.post('/login')
async def login(usuario_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = verificar_hash(usuario_schema.email, usuario_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=404, detail='usuário não encontrado')
    dict_usuario = {'sub': usuario_schema.email}
    access_token = criar_token(dict_usuario)
    refresh_token = criar_token(dict_usuario, timedelta(days=7))
    return {
        'message': 'usuário logado com sucesso',
        'access_token': access_token,
        'refresh_token': refresh_token
    }

@usuario_router.post('/login-form')
async def login_form(oauth_schema: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = verificar_hash(oauth_schema.username, oauth_schema.password, session)
    if not usuario:
        raise HTTPException(status_code=404, detail='usuário não encontrado')
    dict_usuario = {'sub': oauth_schema.username}
    access_token = criar_token(dict_usuario)
    refresh_token = criar_token(dict_usuario, timedelta(days=7))
    return {
        'message': 'usuário logado com sucesso',
        'access_token': access_token,
        'refresh_token': refresh_token
    }

@usuario_router.get('/perfil')
async def perfil(session: Session = Depends(pegar_sessao), usuario: str = Depends(verificar_token)):
    return {
        'usuario': usuario.nome
    }


