# 🚀 Blog API - FastAPI

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![CI/CD](https://github.com/guscassiano/dio_blog/actions/workflows/ci.yml/badge.svg)](https://github.com/guscassiano/dio_blog/actions)

Uma API RESTful assíncrona para gerenciamento de um Blog, construída com as melhores práticas de Engenharia de Software. O projeto contempla autenticação, controle de acesso baseado em papéis (RBAC) e uma suíte completa de testes de integração.

## 💻 Sobre o Projeto

Este projeto foi desenvolvido no bootcamp oferecedo pela **Luíza Labs em parceira DIO** sobre FastAPI para fornecer o backend de uma plataforma de postagens. Implementei recursos a mais como CRUD completo para que usuários se registrem, façam login de forma segura, criem e gerenciem seus próprios posts. Além disso, adicionei um sistema de privilégios onde Administradores possuem controle estendido sobre a moderação do conteúdo e contas de usuários.

## 🛠️ Tecnologias Utilizadas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Assíncrono e de alta performance)
* **Linguagem:** Python 3.14+
* **ORM & Banco de Dados:** SQLAlchemy, Databases (Async) e SQLite
* **Validação de Dados:** Pydantic V2
* **Autenticação:** JWT (JSON Web Tokens) com hashing de senhas via passlib/bcrypt
* **Gerenciamento de Pacotes:** Poetry
* **Testes:** Pytest & HTTPX (Cobertura de rotas e segurança)
* **CI/CD:** GitHub Actions

## ⚙️ Funcionalidades

### 🔐 Autenticação e Segurança
* Login com geração de Token JWT (Bearer).
* Proteção de rotas utilizando `Depends`.
* Controle de papéis (`role: admin` vs `role: user`).
* Segregação de Schemas (DTOs) para evitar vazamento de dados sensíveis.

### 👤 Usuários
* Registro de novos usuários com validação estrita de e-mail.
* Busca de perfil público (ocultando e-mail) e perfil privado (`/users/me`).
* Atualização de dados cadastrais.
* **Soft Delete:** Exclusão lógica de contas (`active=False`), revogando imediatamente o acesso.
* Toggle de suspensão/restauração de contas (Exclusivo para Admins).

### 📝 Posts
* Criação de publicações vinculadas ao autor.
* Listagem global com paginação e filtros dinâmicos (ex: `published=true`).
* Edição e exclusão de posts com travas de segurança (o usuário só pode alterar o próprio post, exceto se for Admin).

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.14 ou superior instalado.
* [Poetry](https://python-poetry.org/) instalado (`pipx install poetry`).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/guscassiano/dio-blog.git
   cd dio-blog
2. **Instale as dependências:**
   ```bash
   poetry install
3. **Inicie o servidor de desenvolvimento:**
   ```bash
   poetry run uvicorn src.main:app --reload
4. **Acesse a documentação interativa:**

    * Swagger UI: http://localhost:8000/docs
    * ReDoc: http://localhost:8000/redoc

   > ⚠️ **Atenção (Teste Local):** Como a API possui múltiplos ambientes configurados, ao acessar o Swagger na sua máquina, lembre-se de clicar no menu dropdown **"Servers"** (no topo da página) e selecionar a opção `http://localhost:8000 - Staging environment`. Caso contrário, os seus testes locais tentarão bater no banco de dados de produção!
## 🧪 Como Rodar os Testes

O projeto possui uma suíte robusta de testes de integração cobrindo Happy Paths e validações de segurança (Sad Paths).

Para executar os testes, utilize o comando:
```bash
poetry run pytest -v
```
_(O banco de dados de testes tests.db será gerado automaticamente em memória/arquivo e limpo após a execução)._

## 👨‍💻 Autor
### Gustavo Cassiano Pinto