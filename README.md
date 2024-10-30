# fastapi_MADR_redis

# MADR Meu Acervo De Romance

***

* crud de usuario
* crud de romancistas (autores)
* crud de livros
* autenticacao via token
* hash de senha
* fila de banco de dados com redis em post de romancista e livro
* versionamento de tabelas do banco de dados

***
  ### tecnologias

  * python = "^3.11"
  * fastapi = {extras = ["standard"], version = "^0.112.0"}
  * uvicorn = "^0.30.5"
  * sqlalchemy = "^2.0.32"
  * pydantic-settings = "^2.4.0"
  * alembic = "^1.13.2"
  * psycopg = {extras = ["binary"], version = "^3.2.1"}
  * pwdlib = {extras = ["argon2"], version = "^0.2.0"}
  * python-multipart = "^0.0.9"
  * pyjwt = "^2.9.0"

***
### dependencia
* Docker
* Docker Compose

***

### comandos
` docker compose up --build `
