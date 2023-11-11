from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'public'}

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".categories_codigo_seq'::regclass)"))
    category_id = Column(String(13), nullable=False, unique=True)
    category_name = Column(String(80), nullable=False, unique=True)
