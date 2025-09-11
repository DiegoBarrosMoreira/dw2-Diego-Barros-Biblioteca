# 📚 Sistema de Biblioteca

Mini-sistema web para gerenciamento de livros em uma biblioteca.

## Tecnologias
- Front-end: HTML5, CSS3 (Flexbox / Grid), JavaScript (ES6)
- Back-end: Python + FastAPI
- Banco: SQLite + SQLAlchemy

## Como rodar

1. Na pasta `backend`, crie um ambiente virtual e instale dependências:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Inicialize o banco e rode o servidor:

```powershell
python -m backend.seed
uvicorn backend.app:app --reload
```

3. Abra `frontend/index.html` no navegador (ou sirva com um servidor estático).

## Endpoints
- `GET /livros` - lista livros
- `POST /livros` - cria livro
- `PUT /livros/{id}` - atualiza livro
- `DELETE /livros/{id}` - exclui livro

## Observações
- API providencia CORS para facilitar testes com o frontend estático.
