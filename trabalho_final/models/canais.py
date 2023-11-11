# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
Base = declarative_base()

class Canais(Base):
    __tablename__ = 'canais'
    __table_args__ = {'schema': 'public'}

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".canais_codigo_seq'::regclass)"))
    channel_id = Column(String(13), unique=True)
    broadcaster_name = Column(ForeignKey('public.usuarios.display_name'), unique=True)
    broadcaster_lang = Column(String(15))
    game_name = Column(String(50))

    usuario = relationship('Usuario', uselist=False)

