from fastapi import FastAPI
from models import Base, engine

app = FastAPI()
Base.metadata.create_all(engine)

from usuarios_routes import usuario_router
app.include_router(usuario_router)