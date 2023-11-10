# categorias.py
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES

Base = declarative_base()

class Categorias(Base):
    __tablename__ = 'categorias'

    id = Column(String(13), primary_key=True)
    name = Column(String(30), nullable=False)

# Obtém as configurações do banco de dados do Django
database_config = DATABASES['default']
database_url = (
    f"postgresql+psycopg2://{database_config['USER']}:{database_config['PASSWORD']}@"
    f"{database_config['HOST']}:{database_config['PORT']}/{database_config['NAME']}"
)

