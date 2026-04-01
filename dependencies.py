from sqlalchemy.orm import Session, sessionmaker
from models import engine, Usuarios
from security import oauth2, SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2), session: Session = Depends(pegar_sessao)):
    print(token)
    try:
        dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_email = dict_info.get('sub')
    except JWTError:
        raise HTTPException(status_code=401, detail='acesso negado')
    usuario = session.query(Usuarios).filter(Usuarios.email==usuario_email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='usuario não encontrado')
    return usuario
    

