# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StreamCategory(Base):
    __tablename__ = 'stream_categories'
    __table_args__ = (
        UniqueConstraint('stream_id', 'category_id'),
        {'schema': 'public'}
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".stream_categories_codigo_seq'::regclass)"))
    stream_id = Column(ForeignKey('public.streams.stream_id'))
    category_id = Column(ForeignKey('public.categories.category_id'))

    category = relationship('Category')
    stream = relationship('Stream')
