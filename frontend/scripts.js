const API = "http://127.0.0.1:8000";

const form = document.getElementById('livro-form');
const tabelaBody = document.querySelector('#livros-table tbody');
const formTitle = document.getElementById('form-title');
const cancelBtn = document.getElementById('cancel-btn');

async function fetchLivros(){
	const res = await fetch(`${API}/livros`);
	const data = await res.json();
	renderTabela(data);
}

function renderTabela(livros){
	tabelaBody.innerHTML = '';
	livros.forEach(l => {
		const tr = document.createElement('tr');
		tr.innerHTML = `
			<td>${l.id}</td>
			<td>${escapeHtml(l.titulo)}</td>
			<td>${escapeHtml(l.autor)}</td>
			<td>${l.ano_publicacao}</td>
			<td>${l.disponivel ? 'Sim' : 'Não'}</td>
			<td class="actions-cell">
				<button data-id="${l.id}" class="edit">Editar</button>
				<button data-id="${l.id}" class="delete">Excluir</button>
			</td>
		`;
		tabelaBody.appendChild(tr);
	});

	tabelaBody.querySelectorAll('.edit').forEach(btn => btn.addEventListener('click', onEdit));
	tabelaBody.querySelectorAll('.delete').forEach(btn => btn.addEventListener('click', onDelete));
}

function escapeHtml(str){
	return String(str).replace(/[&<>"']/g, function(tag){
		const chars = {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"};
		return chars[tag] || tag;
	});
}

async function onEdit(e){
	const id = e.target.dataset.id;
	const res = await fetch(`${API}/livros`);
	const livros = await res.json();
	const livro = livros.find(x => x.id === Number(id));
	if(!livro) return alert('Livro não encontrado');
	document.getElementById('livro-id').value = livro.id;
	document.getElementById('titulo').value = livro.titulo;
	document.getElementById('autor').value = livro.autor;
	document.getElementById('ano_publicacao').value = livro.ano_publicacao;
	document.getElementById('disponivel').checked = livro.disponivel;
	formTitle.textContent = 'Editar Livro';
}

async function onDelete(e){
	if(!confirm('Confirma exclusão do livro?')) return;
	const id = e.target.dataset.id;
	await fetch(`${API}/livros/${id}`, { method: 'DELETE' });
	fetchLivros();
}

form.addEventListener('submit', async (ev) =>{
	ev.preventDefault();
	const id = document.getElementById('livro-id').value;
	const payload = {
		titulo: document.getElementById('titulo').value,
		autor: document.getElementById('autor').value,
		ano_publicacao: Number(document.getElementById('ano_publicacao').value),
		disponivel: document.getElementById('disponivel').checked,
	};

	if(id){
		await fetch(`${API}/livros/${id}`, { method: 'PUT', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
	} else {
		await fetch(`${API}/livros`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
	}

	resetForm();
	fetchLivros();
});

cancelBtn.addEventListener('click', () => { resetForm(); });

function resetForm(){
	document.getElementById('livro-id').value = '';
	document.getElementById('titulo').value = '';
	document.getElementById('autor').value = '';
	document.getElementById('ano_publicacao').value = '';
	document.getElementById('disponivel').checked = true;
	formTitle.textContent = 'Adicionar Livro';
}

window.addEventListener('load', ()=>{ fetchLivros(); });

