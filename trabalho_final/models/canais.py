# canais.py
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES

Base = declarative_base()

class Canais(Base):
    __tablename__ = 'canais'

    id = Column(String(13), primary_key=True)
    broadcaster_name = Column(String(30))
    broadcaster_lang = Column(String(15))
    game_name = Column(String(50))

# Obtém as configurações do banco de dados do Django
database_config = DATABASES['default']
database_url = (
    f"postgresql+psycopg2://{database_config['USER']}:{database_config['PASSWORD']}@"
    f"{database_config['HOST']}:{database_config['PORT']}/{database_config['NAME']}"
)

