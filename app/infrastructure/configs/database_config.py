from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.configs.base_mixin import Base  # Importando a Base daqui

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/seu_banco"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
