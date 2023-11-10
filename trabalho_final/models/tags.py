# tags.py
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tags(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    stream_id = Column(String(13), ForeignKey('streams.stream_id'), nullable=False)
    tag_name = Column(String(30), nullable=False)

    # Adiciona o relacionamento
    stream = relationship('Streams', back_populates='tags')

# Obtém as configurações do banco de dados do Django
database_config = DATABASES['default']
database_url = (
    f"postgresql+psycopg2://{database_config['USER']}:{database_config['PASSWORD']}@"
    f"{database_config['HOST']}:{database_config['PORT']}/{database_config['NAME']}"
)

