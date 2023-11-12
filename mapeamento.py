# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('categories_codigo_seq'::regclass)"))
    category_id = Column(String(13), nullable=False, unique=True)
    category_name = Column(String(80), nullable=False, unique=True)


class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        CheckConstraint("((broadcaster_type)::text = 'affiliate'::text) OR ((broadcaster_type)::text = 'partner'::text) OR ((broadcaster_type)::text = ''::text)"),
        CheckConstraint("((user_type)::text = 'admin'::text) OR ((user_type)::text = 'global mod'::text) OR ((user_type)::text = 'staff'::text) OR ((user_type)::text = ''::text)")
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('usuarios_codigo_seq'::regclass)"))
    user_id = Column(String(13), nullable=False, unique=True)
    login = Column(String(30), nullable=False, unique=True)
    display_name = Column(String(30), nullable=False, unique=True)
    user_type = Column(String(10))
    broadcaster_type = Column(String(10))
    description = Column(Text)
    email = Column(String(30), nullable=False, unique=True)
    created_at = Column(Date)


class Canais(Base):
    __tablename__ = 'canais'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('canais_codigo_seq'::regclass)"))
    channel_id = Column(String(13), unique=True)
    broadcaster_name = Column(ForeignKey('usuarios.display_name'), unique=True)
    broadcaster_lang = Column(String(15))
    game_name = Column(String(50))

    usuario = relationship('Usuario', uselist=False)


class Polls(Base):
    __tablename__ = 'polls'
    __table_args__ = (
        CheckConstraint("((status)::text = 'ACTIVE'::text) OR ((status)::text = 'COMPLETED'::text) OR ((status)::text = 'TERMINATED'::text) OR ((status)::text = 'ARCHIVED'::text) OR ((status)::text = 'MODERATED'::text) OR ((status)::text = 'INVALID'::text)"),
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('polls_codigo_seq'::regclass)"))
    poll_id = Column(String(13))
    title = Column(String(80))
    status = Column(String(10))
    started_at = Column(Date)
    ended_at = Column(Date)
    broadcaster_id = Column(ForeignKey('canais.channel_id'))

    broadcaster = relationship('Canais')


class Streams(Base):
    __tablename__ = 'streams'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('streams_codigo_seq'::regclass)"))
    stream_id = Column(String(13), unique=True)
    broadcaster_name = Column(ForeignKey('canais.broadcaster_name'), nullable=False, unique=True)
    title = Column(String(140), nullable=True)
    started_at = Column(Date)
    viewer_count = Column(Integer)
    stream_lang = Column(String(15))

    canais = relationship('Canais', uselist=False)


class StreamCategory(Base):
    __tablename__ = 'stream_categories'
    __table_args__ = (
        UniqueConstraint('stream_id', 'category_id'),
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('stream_categories_codigo_seq'::regclass)"))
    stream_id = Column(ForeignKey('streams.stream_id'))
    category_id = Column(ForeignKey('categories.category_id'))

    category = relationship('Category')
    stream = relationship('Streams')


class Tags(Base):
    __tablename__ = 'tags'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('tags_codigo_seq'::regclass)"))
    tag_id = Column(String(20), nullable=False, unique=True)
    stream_id = Column(ForeignKey('streams.stream_id'))
    tag_name = Column(String(30))

    stream = relationship('Streams')
