from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'db.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)


@app.route('/livros', methods=['GET'])
def listar_livros():
    conn = get_db_connection()
    cur = conn.execute('SELECT id, titulo, autor, ano_publicacao, disponivel FROM livros')
    rows = cur.fetchall()
    conn.close()
    livros = []
    for r in rows:
        livros.append({
            'id': r['id'],
            'titulo': r['titulo'],
            'autor': r['autor'],
            'ano_publicacao': r['ano_publicacao'],
            'disponivel': bool(r['disponivel']),
        })
    return jsonify(livros)


@app.route('/livros', methods=['POST'])
def criar_livro():
    data = request.get_json() or {}
    required = ['titulo', 'autor', 'ano_publicacao', 'disponivel']
    if not all(k in data for k in required):
        return abort(400, 'Campos ausentes')
    conn = get_db_connection()
    cur = conn.execute('INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES (?, ?, ?, ?)',
                       (data['titulo'], data['autor'], data['ano_publicacao'], int(bool(data['disponivel']))))
    conn.commit()
    id_ = cur.lastrowid
    cur = conn.execute('SELECT id, titulo, autor, ano_publicacao, disponivel FROM livros WHERE id = ?', (id_,))
    row = cur.fetchone()
    conn.close()
    return jsonify({'id': row['id'], 'titulo': row['titulo'], 'autor': row['autor'], 'ano_publicacao': row['ano_publicacao'], 'disponivel': bool(row['disponivel'])}), 201


@app.route('/livros/<int:livro_id>', methods=['PUT'])
def atualizar_livro(livro_id):
    data = request.get_json() or {}
    conn = get_db_connection()
    cur = conn.execute('SELECT id FROM livros WHERE id = ?', (livro_id,))
    if cur.fetchone() is None:
        conn.close()
        return abort(404, 'Livro não encontrado')
    conn.execute('UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ? WHERE id = ?',
                 (data.get('titulo'), data.get('autor'), data.get('ano_publicacao'), int(bool(data.get('disponivel'))), livro_id))
    conn.commit()
    cur = conn.execute('SELECT id, titulo, autor, ano_publicacao, disponivel FROM livros WHERE id = ?', (livro_id,))
    row = cur.fetchone()
    conn.close()
    return jsonify({'id': row['id'], 'titulo': row['titulo'], 'autor': row['autor'], 'ano_publicacao': row['ano_publicacao'], 'disponivel': bool(row['disponivel'])})


@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def excluir_livro(livro_id):
    conn = get_db_connection()
    cur = conn.execute('SELECT id FROM livros WHERE id = ?', (livro_id,))
    if cur.fetchone() is None:
        conn.close()
        return abort(404, 'Livro não encontrado')
    conn.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
    conn.commit()
    conn.close()
    return jsonify({'detail': 'Livro excluído'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
