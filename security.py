from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl='usuarios/login-form')

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
JWT_EXPIRE_TIME = os.getenv('JWT_EXPIRE_TIME')