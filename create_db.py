import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'db.sqlite3'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL,
        disponivel INTEGER NOT NULL DEFAULT 1
    )
    ''')
    # seed data if empty
    cur.execute('SELECT COUNT(1) FROM livros')
    count = cur.fetchone()[0]
    if count == 0:
        exemplos = [
            ('Dom Casmurro', 'Machado de Assis', 1899, 1),
            ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 1943, 1),
            ('1984', 'George Orwell', 1949, 0),
        ]
        cur.executemany('INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES (?, ?, ?, ?)', exemplos)
        conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

if __name__ == '__main__':
    init_db()
