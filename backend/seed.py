from .database import SessionLocal, init_db
from .models import Livro


def seed():
	init_db()
	db = SessionLocal()
	try:
		if db.query(Livro).count() == 0:
			exemplos = [
				Livro(titulo="Dom Casmurro", autor="Machado de Assis", ano_publicacao=1899, disponivel=True),
				Livro(titulo="O Pequeno Príncipe", autor="Antoine de Saint-Exupéry", ano_publicacao=1943, disponivel=True),
				Livro(titulo="1984", autor="George Orwell", ano_publicacao=1949, disponivel=False),
			]
			db.add_all(exemplos)
			db.commit()
	finally:
		db.close()


if __name__ == "__main__":
	seed()
