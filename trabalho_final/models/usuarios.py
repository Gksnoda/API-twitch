from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        CheckConstraint("((broadcaster_type)::text = 'affiliate'::text) OR ((broadcaster_type)::text = 'partner'::text) OR ((broadcaster_type)::text = ''::text)"),
        CheckConstraint("((user_type)::text = 'admin'::text) OR ((user_type)::text = 'global mod'::text) OR ((user_type)::text = 'staff'::text) OR ((user_type)::text = ''::text)"),
        {'schema': 'public'}
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".usuarios_codigo_seq'::regclass)"))
    user_id = Column(String(13), nullable=False, unique=True)
    login = Column(String(30), nullable=False, unique=True)
    display_name = Column(String(30), nullable=False, unique=True)
    user_type = Column(String(10))
    broadcaster_type = Column(String(10))
    description = Column(Text)
    email = Column(String(30), nullable=False, unique=True)
    created_at = Column(Date)
