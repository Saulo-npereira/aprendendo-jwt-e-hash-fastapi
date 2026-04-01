from jose import JWTError, jwt
from security import SECRET_KEY, ALGORITHM, pwd_context, JWT_EXPIRE_TIME
from models import Usuarios
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

def gerar_hash(senha: str):
    return pwd_context.hash(senha)

def verificar_hash(email, senha, session):
    usuario = session.query(Usuarios).filter(Usuarios.email==email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='usuario não encontrado')
    return pwd_context.verify(senha, usuario.senha)

def criar_token(dados_dict: dict, duracao: timedelta = timedelta(minutes=int(JWT_EXPIRE_TIME))):
    copia_dados = dados_dict.copy()
    expire = datetime.now(timezone.utc) + duracao
    copia_dados.update({'exp': expire})
    return jwt.encode(copia_dados,SECRET_KEY, algorithm=ALGORITHM)