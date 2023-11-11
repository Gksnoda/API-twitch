# tags.py
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASES
from sqlalchemy.orm import relationship

Base = declarative_base()

class Tags(Base):
    __tablename__ = 'tags'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('tags_codigo_seq'::regclass)"))
    tag_id = Column(String(20), nullable=False, unique=True)
    stream_id = Column(ForeignKey('streams.stream_id'))
    tag_name = Column(String(30))

    stream = relationship('Stream')
