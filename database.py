from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Esto creará el archivo biblioteca.db en tu carpeta actual
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

# El engine es el motor que habla con el archivo .db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# La sesión es lo que usaremos para hacer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que heredarán nuestros modelos de base de datos
Base = declarative_base()