from fastapi import FastAPI
from madr.routers import auth, romancista, users, livros

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(romancista.router)
app.include_router(livros.router)
