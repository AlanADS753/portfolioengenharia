from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

# Função para carregar tarefas do arquivo
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Função para salvar tarefas
def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Rota para criar uma nova tarefa
@app.route('/tasks', methods=['POST'])
def create_task():
    tasks = load_tasks()
    data = request.json
    new_task = {
        "id": len(tasks) + 1,
        "titulo": data.get("titulo"),
        "descricao": data.get("descricao"),
        "status": data.get("status", "A Fazer")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201
