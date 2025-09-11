from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Livro(Base):
	__tablename__ = "livros"

	id = Column(Integer, primary_key=True, index=True)
	titulo = Column(String, nullable=False)
	autor = Column(String, nullable=False)
	ano_publicacao = Column(Integer, nullable=False)
	disponivel = Column(Boolean, default=True)
