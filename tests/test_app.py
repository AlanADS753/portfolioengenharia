import pytest
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app 

@pytest.fixture
def client():
    # Configura o aplicativo Flask para modo de teste
    app.config['TESTING'] = True
    
    # Define um arquivo de dados temporário exclusivo para os testes
    
    temp_data_file = 'test_tasks.json'
    
    # Guarda o caminho original do DATA_FILE para restaurar após os testes
    original_data_file_path = app.config.get('DATA_FILE', 'tasks.json') # Usa 'tasks.json' como fallback se não estiver definido
    # Sobrescreve o DATA_FILE do app para usar o arquivo temporário durante os testes
    app.config['DATA_FILE'] = temp_data_file

    # Garante que o arquivo de dados temporário esteja limpo antes de cada teste
    if os.path.exists(temp_data_file):
        os.remove(temp_data_file)

    # Cria um cliente de teste Flask para fazer requisições HTTP simuladas
    with app.test_client() as client:
        yield client 

    # Após o teste ser concluído, limpa o arquivo de dados temporário
    if os.path.exists(temp_data_file):
        os.remove(temp_data_file)
    
    # Restaura o DATA_FILE original no aplicativo Flask
    app.config['DATA_FILE'] = original_data_file_path


# Testes para a rota POST /tasks (Criar Tarefa) 

def test_create_task_success(client):
    """
    Testa se uma nova tarefa pode ser criada com sucesso (status 201)
    e se os dados retornados e salvos no arquivo estão corretos.
    """
    response = client.post('/tasks', json={
        "titulo": "Comprar Pão",
        "descricao": "Pão francês na padaria",
        "status": "A Fazer"
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert data['titulo'] == "Comprar Pão"
    assert data['descricao'] == "Pão francês na padaria"
    assert data['status'] == "A Fazer"
    assert data['id'] == 1 # Espera que o primeiro ID seja 1

    # Verifica se a tarefa foi realmente salva no arquivo de dados de teste
    tasks_in_file = []
    # Acessa o caminho do arquivo de dados através de app.config
    if os.path.exists(app.config['DATA_FILE']):
        with open(app.config['DATA_FILE'], 'r', encoding='utf-8') as f:
            tasks_in_file = json.load(f)
    assert len(tasks_in_file) == 1
    assert tasks_in_file[0]['titulo'] == "Comprar Pão"
    assert tasks_in_file[0]['id'] == 1

def test_create_task_default_status(client):
    """
    Testa se o status padrão 'A Fazer' é aplicado quando o campo 'status' não é fornecido.
    """
    response = client.post('/tasks', json={
        "titulo": "Tarefa sem status",
        "descricao": "Esta tarefa não especifica um status inicial."
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == "A Fazer"

def test_create_task_missing_title(client):
    """
    Testa se o sistema retorna erro 400 (Bad Request) quando o título está faltando.
    """
    response = client.post('/tasks', json={
        "descricao": "Sem título, não deve ser criada."
    })
    assert response.status_code == 400
    assert json.loads(response.data)['message'] == "Título da tarefa é obrigatório"


# Testes para a rota GET /tasks (Listar Todas as Tarefas) 

def test_get_tasks_empty(client):
    """
    Testa se a lista de tarefas está vazia quando nenhuma tarefa foi criada.
    """
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0
    assert data == [] 


def test_get_tasks_multiple(client):
    """
    Testa se múltiplas tarefas são retornadas corretamente na lista.
    """
    client.post('/tasks', json={"titulo": "Tarefa Um", "status": "A Fazer"})
    client.post('/tasks', json={"titulo": "Tarefa Dois", "status": "Concluída"})

    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert len(data) == 2
    assert data[0]['titulo'] == "Tarefa Um"
    assert data[1]['titulo'] == "Tarefa Dois"
    assert data[0]['id'] == 1
    assert data[1]['id'] == 2


#  Testes para a rota GET /tasks/<int:task_id> (Obter Tarefa por ID)

def test_get_specific_task_found(client):
    """
    Testa se uma tarefa específica é retornada quando o ID existe.
    """
    client.post('/tasks', json={"titulo": "Tarefa para Buscar", "descricao": "Detalhes específicos"})
    client.post('/tasks', json={"titulo": "Outra Tarefa"}) # Cria uma segunda para garantir que busca o ID certo

    response = client.get('/tasks/1') # Busca a tarefa com ID 1
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['titulo'] == "Tarefa para Buscar"
    assert data['id'] == 1


def test_get_specific_task_not_found(client):
    """
    Testa se um erro 404 é retornado quando a tarefa não é encontrada pelo ID.
    """
    response = client.get('/tasks/999') 
    assert response.status_code == 404
    assert json.loads(response.data)['message'] == "Tarefa não encontrada"


#  Testes para a rota PUT /tasks/<int:task_id> (Atualizar Tarefa) 

def test_update_task_success(client):
    """
    Testa a atualização bem-sucedida de todos os campos de uma tarefa.
    """
    client.post('/tasks', json={"titulo": "Tarefa Velha", "descricao": "Descrição Antiga", "status": "A Fazer"})

    update_data = {
        "titulo": "Tarefa Nova",
        "descricao": "Nova Descrição",
        "status": "Em Andamento"
    }
    response = client.put('/tasks/1', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['titulo'] == "Tarefa Nova"
    assert data['descricao'] == "Nova Descrição"
    assert data['status'] == "Em Andamento"
    assert data['id'] == 1 

    # Verifica se a atualização persistiu no arquivo de dados de teste
    tasks_in_file = []
    # Acessa o caminho do arquivo de dados através de app.config
    if os.path.exists(app.config['DATA_FILE']):
        with open(app.config['DATA_FILE'], 'r', encoding='utf-8') as f:
            tasks_in_file = json.load(f)
    assert len(tasks_in_file) == 1
    assert tasks_in_file[0]['titulo'] == "Tarefa Nova"


def test_update_task_partial(client):
    """
    Testa a atualização parcial de uma tarefa (apenas alguns campos são enviados).
    Os campos não enviados não devem ser alterados.
    """
    client.post('/tasks', json={"titulo": "Tarefa Parcial", "descricao": "Manter", "status": "A Fazer"})

    update_data = {
        "status": "Concluída" 
    }
    response = client.put('/tasks/1', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['titulo'] == "Tarefa Parcial" 
    assert data['descricao'] == "Manter"     
    assert data['status'] == "Concluída"     


def test_update_task_not_found(client):
    """
    Testa a tentativa de atualização de uma tarefa que não existe (status 404).
    """
    response = client.put('/tasks/999', json={"titulo": "Não existe"})
    assert response.status_code == 404
    assert json.loads(response.data)['message'] == "Tarefa não encontrada"

def test_update_task_no_data(client):
    """
    Testa se o sistema retorna erro 400 (Bad Request) quando nenhum dado é fornecido para atualização.
    """
    client.post('/tasks', json={"titulo": "Tarefa para Atualizar", "status": "A Fazer"})
    response = client.put('/tasks/1', json={}) # Corpo vazio
    assert response.status_code == 400
    assert json.loads(response.data)['message'] == "Nenhum dado fornecido para atualização"


# Testes para a rota DELETE /tasks/<int:task_id> (Deletar Tarefa) 

def test_delete_task_success(client):
    """
    Testa a deleção bem-sucedida de uma tarefa.
    """
    client.post('/tasks', json={"titulo": "Para Deletar 1"})
    client.post('/tasks', json={"titulo": "Para Deletar 2"}) # Adiciona outra para verificar a remoção correta

    response = client.delete('/tasks/1') # Deleta a tarefa com ID 1
    assert response.status_code == 204 

    # Verifica se a tarefa foi realmente removida da lista e se a lista está correta
    response_get_after_delete = client.get('/tasks')
    data_after_delete = json.loads(response_get_after_delete.data)
    assert len(data_after_delete) == 1 
    assert data_after_delete[0]['titulo'] == "Para Deletar 2" 


def test_delete_task_not_found(client):
    """
    Testa a deleção de uma tarefa que não existe (status 404).
    """
    response = client.delete('/tasks/999') # ID que certamente não existe
    assert response.status_code == 404
    assert json.loads(response.data)['message'] == "Tarefa não encontrada"

def test_delete_task_empty_list(client):
    """
    Testa a deleção de uma tarefa quando a lista de tarefas está vazia.
    """
    response = client.delete('/tasks/1') # Tenta deletar sem ter nenhuma tarefa
    assert response.status_code == 404
    assert json.loads(response.data)['message'] == "Tarefa não encontrada"
