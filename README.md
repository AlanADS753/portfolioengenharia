# Sistema de Gerenciamento de Tarefas Ágil (TechFlow Solutions)

## 1. Objetivo do Projeto

O objetivo deste projeto é desenvolver um sistema básico de gerenciamento de tarefas, utilizando princípios de metodologias ágeis. Este sistema permitirá acompanhar o fluxo de trabalho, gerenciar tarefas (CRUD - Criar, Ler, Atualizar, Deletar) e demonstrar conceitos de engenharia de software como controle de qualidade e gestão de mudanças.

## 2. Escopo do Projeto

A versão inicial deste sistema focará em um CRUD completo para tarefas, permitindo as seguintes operações:
* **Criação:** Adicionar novas tarefas com título, descrição e status.
* **Leitura:** Visualizar todas as tarefas ou uma tarefa específica por ID.
* **Atualização:** Modificar informações de tarefas existentes.
* **Exclusão:** Remover tarefas do sistema.

## 3. Metodologia Adotada

Este projeto segue uma abordagem ágil, utilizando princípios do **Kanban** para gerenciamento do fluxo de trabalho. As tarefas são organizadas e acompanhadas na aba [Projects do GitHub]([https://github.com/users/AlanADS753/projects/5/views/1]).

## 4. Requisitos do Sistema

### 4.1. Requisitos Funcionais (RF)

* **RF001 - Criação de Tarefa:** O sistema deve permitir que um usuário crie uma nova tarefa, fornecendo um título, uma descrição e, opcionalmente, um status.
* **RF002 - Visualização de Tarefas:** O sistema deve permitir que um usuário visualize a lista completa de todas as tarefas existentes.
* **RF003 - Visualização de Tarefa por ID:** O sistema deve permitir que um usuário visualize os detalhes de uma tarefa específica, fornecendo seu identificador único (ID).
* **RF004 - Atualização de Tarefa:** O sistema deve permitir que um usuário atualize o título, a descrição e/ou o status de uma tarefa existente, fornecendo seu identificador único (ID) e os novos dados.
* **RF005 - Exclusão de Tarefa:** O sistema deve permitir que um usuário exclua uma tarefa existente, fornecendo seu identificador único (ID).
* **RF006 - Persistência de Dados:** O sistema deve armazenar as informações das tarefas de forma persistente (neste caso, em um arquivo `tasks.json`) para que os dados não sejam perdidos ao reiniciar a aplicação.

### 4.2. Requisitos Não Funcionais (RNF)

* **RNF001 - Performance:** O sistema deve responder às requisições da API em um tempo razoável (ex: abaixo de 500ms para operações CRUD básicas).
* **RNF002 - Usabilidade (API):** A API deve ser intuitiva e seguir padrões RESTful para facilitar o consumo por outras aplicações.
* **RNF003 - Confiabilidade:** O sistema deve garantir a integridade dos dados das tarefas, evitando corrupção ou perda de informações.
* **RNF004 - Manutenibilidade:** O código-fonte deve ser modular, claro, com comentários explicativos e seguir boas práticas de programação para facilitar futuras manutenções e evoluções.
* **RNF005 - Testabilidade:** O sistema deve possuir testes automatizados que garantam o correto funcionamento das funcionalidades implementadas.
* **RNF006 - Segurança (Básico):** O acesso à API deve ser via HTTPS (considerando que na implantação real, e não no desenvolvimento local, isso seria configurado).
* **RNF007 - Escalabilidade (Básico):** A arquitetura inicial deve permitir uma futura expansão para um volume maior de dados e usuários, sem a necessidade de reestruturação completa (considerando a evolução de JSON para DB, por exemplo).
* **RNF008 - Portabilidade:** O sistema deve ser capaz de ser executado em diferentes sistemas operacionais (Windows, Linux) com as mesmas dependências e configurações.

## 5. Modelagem UML

A arquitetura do sistema foi modelada utilizando os seguintes diagramas UML, conforme solicitado:

### 5.1. Diagrama de Casos de Uso

Representa as funcionalidades do sistema sob a perspectiva do usuário.

![Diagrama de Casos de Uso](docs/diagrams/DiagramaUso.png)


### 5.2. Diagrama de Classes

Descreve a estrutura estática do sistema em termos de suas classes, atributos e seus relacionamentos.

![Diagrama de Classes](docs/diagrams/DiagramaClasse.png)
