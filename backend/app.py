from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from . import models, database

app = FastAPI(title="Sistema de Biblioteca")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class LivroCreate(BaseModel):
	titulo: str
	autor: str
	ano_publicacao: int
	disponivel: bool = True


class LivroUpdate(BaseModel):
	titulo: str
	autor: str
	ano_publicacao: int
	disponivel: bool


class LivroOut(BaseModel):
	id: int
	titulo: str
	autor: str
	ano_publicacao: int
	disponivel: bool

	class Config:
		orm_mode = True


@app.on_event("startup")
def startup():
	database.init_db()


@app.get("/livros", response_model=List[LivroOut])
def listar_livros():
	db: Session = database.SessionLocal()
	try:
		livros = db.query(models.Livro).all()
		return livros
	finally:
		db.close()


@app.post("/livros", response_model=LivroOut)
def criar_livro(livro: LivroCreate):
	db: Session = database.SessionLocal()
	try:
		novo = models.Livro(
			titulo=livro.titulo,
			autor=livro.autor,
			ano_publicacao=livro.ano_publicacao,
			disponivel=livro.disponivel,
		)
		db.add(novo)
		db.commit()
		db.refresh(novo)
		return novo
	finally:
		db.close()


@app.put("/livros/{livro_id}", response_model=LivroOut)
def atualizar_livro(livro_id: int, dados: LivroUpdate):
	db: Session = database.SessionLocal()
	try:
		livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
		if not livro:
			raise HTTPException(status_code=404, detail="Livro não encontrado")
		livro.titulo = dados.titulo
		livro.autor = dados.autor
		livro.ano_publicacao = dados.ano_publicacao
		livro.disponivel = dados.disponivel
		db.commit()
		db.refresh(livro)
		return livro
	finally:
		db.close()


@app.delete("/livros/{livro_id}")
def excluir_livro(livro_id: int):
	db: Session = database.SessionLocal()
	try:
		livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
		if not livro:
			raise HTTPException(status_code=404, detail="Livro não encontrado")
		db.delete(livro)
		db.commit()
		return {"detail": "Livro excluído"}
	finally:
		db.close()
