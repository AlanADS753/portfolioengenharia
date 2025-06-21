from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json' # Define o nome do arquivo de dados para persistência

# Função para carregar tarefas do arquivo
def load_tasks():
    """
    Carrega as tarefas do arquivo JSON.
    Se o arquivo não existir ou estiver vazio/corrompido, retorna uma lista vazia.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Retorna lista vazia se o arquivo estiver vazio ou contiver JSON inválido
        return []
    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")
        return []

# Função para salvar tarefas no arquivo
def save_tasks(tasks):
    """Salva a lista de tarefas no arquivo JSON, formatando-o para leitura."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        # ensure_ascii=False permite que caracteres UTF-8 (como acentos) sejam salvos diretamente
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# Rota para criar uma nova tarefa (POST /tasks)
@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Cria uma nova tarefa a partir dos dados JSON recebidos.
    Requer 'titulo' e 'descricao'. 'status' é opcional (padrão: 'A Fazer').
    Retorna a tarefa criada com status 201 Created.
    """
    tasks = load_tasks()
    data = request.json

    # Validação básica: Título é obrigatório
    if not data or not data.get("titulo"):
        return jsonify({"message": "Título da tarefa é obrigatório"}), 400

    # Gera um ID simples (incrementa o último ID ou começa do 1)
    # Nota: Em sistemas reais, usaria UUIDs ou IDs gerados por banco de dados
    new_id = 1
    if tasks:
        # Encontra o maior ID existente e adiciona 1
        new_id = max(task['id'] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "titulo": data.get("titulo"),
        "descricao": data.get("descricao"),
        "status": data.get("status", "A Fazer") # Define 'A Fazer' como status padrão
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

# Rota para listar todas as tarefas (GET /tasks)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retorna uma lista contendo todas as tarefas existentes.
    Retorna status 200 OK.
    """
    tasks = load_tasks()
    return jsonify(tasks), 200

# Rota para obter uma tarefa por ID (GET /tasks/<int:task_id>)
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtém os detalhes de uma tarefa específica pelo seu ID.
    Retorna a tarefa e status 200 OK, ou mensagem de erro e status 404 Not Found se não encontrada.
    """
    tasks = load_tasks()
    # Usa a função next() para encontrar a tarefa, ou None se não houver correspondência
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({"message": "Tarefa não encontrada"}), 404

# Rota para atualizar uma tarefa (PUT /tasks/<int:task_id>)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Atualiza os campos de uma tarefa existente pelo seu ID.
    Requer um JSON com os campos a serem atualizados (titulo, descricao, status).
    Retorna a tarefa atualizada com status 200 OK, ou mensagem de erro e status 404 Not Found.
    """
    tasks = load_tasks()
    data = request.json
    
    if not data:
        return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

    task_found = False
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            # Atualiza apenas os campos que foram fornecidos na requisição JSON
            tasks[i]['titulo'] = data.get('titulo', task['titulo'])
            tasks[i]['descricao'] = data.get('descricao', task['descricao'])
            tasks[i]['status'] = data.get('status', task['status'])
            save_tasks(tasks)
            task_found = True
            return jsonify(tasks[i]), 200
    return jsonify({"message": "Tarefa não encontrada"}), 404

# Rota para deletar uma tarefa (DELETE /tasks/<int:task_id>)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Deleta uma tarefa existente pelo seu ID.
    Retorna mensagem de sucesso e status 204 No Content se deletada,
    ou mensagem de erro e status 404 Not Found se não encontrada.
    """
    tasks = load_tasks()
    initial_len = len(tasks)
    # Cria uma nova lista contendo todas as tarefas, exceto a que será deletada
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < initial_len:
        return jsonify({"message": "Tarefa deletada com sucesso"}), 204 
    return jsonify({"message": "Tarefa não encontrada"}), 404

if __name__ == '__main__':
    
    app.run(debug=True)

