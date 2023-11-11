# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
class Poll(Base):
    __tablename__ = 'polls'
    __table_args__ = (
        CheckConstraint("((status)::text = 'ACTIVE'::text) OR ((status)::text = 'COMPLETED'::text) OR ((status)::text = 'TERMINATED'::text) OR ((status)::text = 'ARCHIVED'::text) OR ((status)::text = 'MODERATED'::text) OR ((status)::text = 'INVALID'::text)"),
        {'schema': 'public'}
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".polls_codigo_seq'::regclass)"))
    poll_id = Column(String(13))
    title = Column(String(80), nullable=False)
    status = Column(String(10))
    started_at = Column(Date)
    ended_at = Column(Date)
    votes = Column(Integer)
    broadcaster_id = Column(ForeignKey('public.canais.channel_id'))

    broadcaster = relationship('Canais')
