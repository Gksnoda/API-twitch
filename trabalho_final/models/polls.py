# polls.py
from sqlalchemy import Column, String, Enum, Date, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES

Base = declarative_base()

class Polls(Base):
    __tablename__ = 'polls'

    id = Column(String(13), primary_key=True)
    title = Column(String(80), nullable=False)
    STATUS_CHOICES = ('ACTIVE', 'COMPLETED', 'TERMINATED', 'ARCHIVED', 'MODERATED', 'INVALID')
    status = Column(Enum(*STATUS_CHOICES, name='poll_status_enum'), nullable=False)
    started_at = Column(Date, nullable=False)
    ended_at = Column(Date, nullable=False)
    votes = Column(Integer, nullable=False)

# Obtém as configurações do banco de dados do Django
database_config = DATABASES['default']
database_url = (
    f"postgresql+psycopg2://{database_config['USER']}:{database_config['PASSWORD']}@"
    f"{database_config['HOST']}:{database_config['PORT']}/{database_config['NAME']}"
)

