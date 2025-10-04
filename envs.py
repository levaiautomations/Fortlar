import os
from dotenv import load_dotenv
from pydantic import SecretStr

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações do Banco de Dados
# Banco de Dados (PostgreSQL)
SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:postgres@localhost:5432/sistema_pedidos'

# Pool de Conexão
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
SQLALCHEMY_POOL_TIMEOUT=30
SQLALCHEMY_POOL_RECYCLE=1800
SQLALCHEMY_POOL_PRE_PING=True

# Logs do SQL
SQLALCHEMY_SHOW_SQL=True

# JWT
JWT_SECRET_KEY='sua_chave_secreta_aqui'
JWT_ALGORITHM='HS256'
JWT_EXPIRATION_MINUTES=60


MAIL_USERNAME='marcio.levada@exactaworks.com.br'
MAIL_PASSWORD='uzzf gydt mliz ryey'
MAIL_FROM="marcio.levada@exactaworks.com.br"
MAIL_PORT=587
MAIL_SERVER="smtp.gmail.com"
