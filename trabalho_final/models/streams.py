# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Stream(Base):
    __tablename__ = 'streams'
    __table_args__ = {'schema': 'public'}

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".streams_codigo_seq'::regclass)"))
    stream_id = Column(String(13), unique=True)
    broadcaster_name = Column(ForeignKey('public.canais.broadcaster_name'), nullable=False, unique=True)
    title = Column(String(140), nullable=False)
    started_at = Column(Date)
    viewer_count = Column(Integer)
    stream_lang = Column(String(15))

    canais = relationship('Canais', uselist=False)