
# Sistema de Agendamento de Quadras Esportivas

## 📖 Sobre o Projeto

Este projeto é uma aplicação web desenvolvida como trabalho final para a disciplina de **Banco de Dados II** do curso de Ciência da Computação da UDESC. O sistema tem como objetivo gerenciar o agendamento de quadras esportivas, o controle de usuários, recursos e eventos em um ambiente universitário.

A arquitetura do sistema segue o padrão de **3 camadas**, separando claramente as responsabilidades:

1.  **Camada de Apresentação (View):** Interface web construída com Flask e HTML/CSS/JS, responsável por interagir com o usuário.
2.  **Camada de Lógica de Negócios (Service):** Onde as regras de negócio são aplicadas. Esta camada orquestra as operações, validando dados e controlando o fluxo da aplicação.
3.  **Camada de Acesso a Dados (DAO):** Responsável por toda a comunicação com o banco de dados PostgreSQL, abstraindo as queries SQL do resto do sistema.

---

## ✨ Funcionalidades

O sistema possui dois níveis de acesso principais: **Usuário Padrão (Aluno)** e **Administrador**.

### Para Usuários
- 🔑 **Autenticação:** Sistema de login e cadastro seguro.
- 📅 **Meus Agendamentos:** Visualização do histórico de agendamentos pessoais.
- 🆕 **Novo Agendamento:** Fluxo completo para agendar uma quadra:
    1.  Seleção do Ginásio.
    2.  Seleção da Quadra.
    3.  Visualização da grade de horários da semana com os períodos já ocupados.

### Para Administradores (Painel de Controle)
O administrador tem acesso a um painel completo para gerenciar todo o ecossistema do sistema:

- 👥 **Gerenciamento de Usuários:**
    - Visualizar todos os usuários (Alunos, Funcionários, Admins).
    - Criar novos usuários de qualquer tipo através de um formulário dinâmico.
    - Ativar e Desativar o acesso de usuários.
    - Excluir usuários permanentemente.

- 🏟️ **Gerenciamento de Recursos:**
    - **Ginásios:** CRUD completo (Criar, Ler, Atualizar, Excluir).
    - **Quadras:** CRUD completo e alteração de status (`disponivel`, `manutencao`, `interditada`).
    - **Materiais Esportivos:** CRUD completo para controle de inventário.
    - **Esportes:** CRUD completo e uma interface para associar/desassociar esportes a quadras específicas.

- 📋 **Gerenciamento de Atividades:**
    - **Visão Geral de Agendamentos:** Visualizar todos os agendamentos de todos os usuários.
    - **Cancelar Agendamentos:** Cancelar qualquer agendamento em nome de um usuário.
    - **Gerenciar Chamados:** Visualizar e resolver (excluir) chamados de manutenção abertos pelos usuários.
    - **Gerenciar Eventos:** Criar eventos (únicos ou recorrentes) que bloqueiam quadras em datas específicas, com a possibilidade de designar um admin organizador.

---

## 💻 Tecnologias Utilizadas

- **Backend:** Python 3
- **Framework Web:** Flask
- **Banco de Dados:** PostgreSQL
- **Conector do Banco:** Psycopg2
- **Frontend:** HTML5, CSS3, JavaScript

---

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma para refletir a arquitetura em camadas:

```
sistema_agendamentos_quadras/
│
├── camada_dados/
│   ├── __init__.py
│   ├── db_config.py        # Configuração da conexão com o banco
│   ├── agendamento_dao.py
│   ├── chamado_dao.py
│   ├── esporte_dao.py
│   ├── evento_dao.py
│   ├── ginasio_dao.py
│   ├── material_dao.py
│   └── quadra_dao.py
│   └── usuario_dao.py      # DAOs: Classes que executam as queries SQL
│
├── camada_negocio/
│   ├── __init__.py
│   └── servicos.py         # Services: Classes com as regras de negócio
│
├── modelos/
│   ├── __init__.py
│   ├── ginasio.py
│   ├── quadra.py
│   └── usuario.py          # Models: Classes Python que representam as tabelas
│
├── static/
│   └── css/
│       └── padrao.css      # Arquivos estáticos (CSS, JS futuro, imagens)
│
├── templates/
│   ├── layout.html         # Template base para a área logada
│   ├── layout_externo.html # Template base para login/cadastro
│   └── ...                 # Demais arquivos HTML
│
├── app.py                  # Arquivo principal da aplicação Flask (controlador de rotas)
├── requirements.txt        # Lista de dependências Python
└── README.md               # Este arquivo
```

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos
- Python 3.8 ou superior
- PostgreSQL instalado e em execução

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    (Primeiro, certifique-se de ter um arquivo `requirements.txt`. Se não tiver, gere-o com o comando `pip freeze > requirements.txt`)
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    - Crie um novo banco de dados no PostgreSQL (ex: `udesc_quadras`).
    - Abra o arquivo `camada_dados/db_config.py` e altere as credenciais de conexão para as suas:
      ```python
      conexao = psycopg2.connect(
          dbname="seu_banco_de_dados",
          user="seu_usuario_postgres",
          password="sua_senha_postgres",
          host="localhost",
          port="5432"
      )
      ```
    - Execute o script SQL fornecido (`seu_script.sql`) para criar todas as tabelas no seu banco de dados.

5.  **Execute a Aplicação:**
    ```bash
    python app.py
    ```
    O servidor estará em execução em `http://127.0.0.1:5000`.

---

## 👥 Autores

Este projeto foi desenvolvido por:
*   Gustavo de Souza
*   José Augusto Laube
