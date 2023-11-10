# usuarios.py
from sqlalchemy import Column, String, Enum, Text, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import DATABASES

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(String(13), primary_key=True)
    login = Column(String(30), nullable=False)
    display_name = Column(String(30))
    TYPE_CHOICES = ('admin', 'global mod', 'staff', '')
    type = Column(Enum(*TYPE_CHOICES, name='user_type_enum'), nullable=False)
    BROADCASTER_TYPE_CHOICES = ('affiliate', 'partner')
    broadcaster_type = Column(Enum(*BROADCASTER_TYPE_CHOICES, name='broadcaster_type_enum'), nullable=False)
    description = Column(Text)
    email = Column(String(30), unique=True)
    created_at = Column(Date)

    # Adiciona os relacionamentos
    streams = relationship('Streams', back_populates='usuario')

# Obtém as configurações do banco de dados do Django
database_config = DATABASES['default']
database_url = (
    f"postgresql+psycopg2://{database_config['USER']}:{database_config['PASSWORD']}@"
    f"{database_config['HOST']}:{database_config['PORT']}/{database_config['NAME']}"
)

