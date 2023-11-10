# streams.py
from sqlalchemy import Column, String, ForeignKey, Date, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import DATABASES

Base = declarative_base()

class Streams(Base):
    __tablename__ = 'streams'

    stream_id = Column(String(13), primary_key=True)
    user_name = Column(String(13), ForeignKey('usuarios.display_name'), nullable=False)
    game_name = Column(String(50), ForeignKey('categorias.name'), nullable=False)
    title = Column(String(50), nullable=False)
    started_at = Column(Date, nullable=False)
    viewer_count = Column(Integer, nullable=False)
    language = Column(String(13), nullable=False)

    # Adiciona os relacionamentos
    usuario = relationship('Usuarios', back_populates='streams')
    categoria = relationship('Categorias', back_populates='streams')

# Obtém as configurações do banco de dados do Django
database_config = DATABASES['default']
database_url = (
    f"postgresql+psycopg2://{database_config['USER']}:{database_config['PASSWORD']}@"
    f"{database_config['HOST']}:{database_config['PORT']}/{database_config['NAME']}"
)

