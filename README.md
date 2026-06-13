HDB
# Task Manager (Flask)

Aplicação web simples para gerenciar suas tarefas (To-Do), com autenticação de usuários.
Construída com Flask, SQLAlchemy, Flask-Login e Bootstrap.

## Funcionalidades

- Cadastro e autenticação de usuários (senha com hash via Bcrypt)
- Proteção de rotas: páginas internas exigem login
- CRUD completo de tarefas (criar, listar, atualizar e excluir)
- Configurações de conta: alterar nome de usuário e senha
- Páginas de erro customizadas (404 / 403 / 500)

## Tecnologias

| Camada | Stack |
|--------|-------|
| Backend | Flask 3.0.3, Werkzeug 3.0.6 |
| ORM / Banco | Flask-SQLAlchemy 3.1.1 (SQLite) |
| Autenticação | Flask-Login 0.6.3, Flask-Bcrypt 1.0.1 |
| Formulários | Flask-WTF 1.2.1, WTForms 3.1.2 |
| Frontend | Jinja2 3.1.4 + Bootstrap |
| Testes | pytest, pytest-cov |

---

## Pré-requisitos

- Python 3.10+ (testado com Python 3.14)
- `pip` e `venv`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/jaimeneto85/Task-Manager-using-Flask.git
   cd Task-Manager-using-Flask
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. Instale as dependências da aplicação:

   ```bash
   pip3 install -r requirements.txt
   ```

## Como executar a aplicação

```bash
cd todo_project
python run.py
```

A aplicação ficará disponível em **http://127.0.0.1:5000**. O banco SQLite
(`instance/site.db`) é criado automaticamente no primeiro boot.

### Configuração por variáveis de ambiente (opcional)

A aplicação roda com padrões seguros para desenvolvimento, mas aceita
configuração via ambiente:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | valor de desenvolvimento | Chave usada para sessões/CSRF |
| `DATABASE_URI` | `sqlite:///site.db` | URI de conexão do banco |
| `TESTING` | `False` | Quando `1`, ativa modo de teste e desliga CSRF |

```bash
export SECRET_KEY="sua-chave-secreta"
export DATABASE_URI="sqlite:///site.db"
```

---

## Como executar os testes

A suíte de testes usa **pytest** com **pytest-cov** e impõe um gate mínimo de
**90% de cobertura** (atualmente em **100%**).

1. Instale as dependências de teste (uma única vez):

   ```bash
   pip install -r requirements-dev.txt
   ```

2. Rode a suíte completa a partir da **raiz do projeto**:

   ```bash
   pytest
   ```

O `pytest.ini` já habilita o relatório de cobertura e o gate `--cov-fail-under=90`,
então o comando acima roda os testes e valida a cobertura automaticamente.

### Comandos úteis

```bash
pytest -v                                   # saída detalhada por teste
pytest todo_project/tests/test_models.py    # roda um arquivo específico
pytest -k login                             # roda testes que casam com "login"
pytest --cov-report=html                    # gera relatório HTML em htmlcov/
```

Saída esperada:

```
47 passed
Required test coverage of 90% reached. Total coverage: 100.00%
```

| Módulo | Cobertura |
|--------|-----------|
| `todo_project/__init__.py` | 100% |
| `todo_project/forms.py` | 100% |
| `todo_project/models.py` | 100% |
| `todo_project/routes.py` | 100% |

---

## Telas da aplicação

### Página Inicial / Sobre
Página pública de apresentação da aplicação.

![Página Sobre](output/about.jpg)

### Cadastro
Crie uma conta informando usuário e senha. Caso já tenha conta, faça login.

![Página de Cadastro](output/register.jpg)

### Proteção de Rotas
Sem login, qualquer tentativa de acesso a páginas internas redireciona para o
login com um aviso.

![Acesso Inválido](output/invalid-access.jpg)

### Após o Login
Ao autenticar, você é levado à lista das suas tarefas.

![Após o Login](output/after-login.jpg)

### Adicionar Tarefa
Use o link **Add Task** na barra lateral para cadastrar novas tarefas.

![Adicionar Tarefa](output/add-task.jpg)

### Ver Todas as Tarefas
O link **View All Tasks** lista suas tarefas, com botões para **Atualizar** e
**Excluir** cada uma.

![Todas as Tarefas](output/all-tasks.jpg)

### Configurações da Conta
Altere seu nome de usuário e senha pelo menu do usuário na barra de navegação.

![Configurações da Conta](output/account-settings.jpg)

---

## Estrutura do projeto

```
Task-Manager-using-Flask/
├── requirements.txt              # dependências da aplicação
├── requirements-dev.txt          # dependências de teste
├── pytest.ini                    # configuração do pytest + cobertura
├── output/                       # imagens usadas no README
└── todo_project/
    ├── run.py                    # ponto de entrada
    └── todo_project/
        ├── __init__.py           # app, config, db, login manager, bcrypt
        ├── models.py             # modelos User e Task
        ├── routes.py             # rotas (auth + CRUD de tarefas)
        ├── forms.py              # formulários Flask-WTF
        ├── templates/            # templates Jinja2
        ├── static/               # CSS e Bootstrap
        └── tests/                # suíte de testes (pytest)
```
