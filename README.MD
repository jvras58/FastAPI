<h1 align="center">
  <a href="#">Projeto com FastAPI</a>
</h1>

<p align="center">
  Bem-vindo! Este é um projeto para desenvolver uma API RESTful utilizando o framework FastAPI, com foco em autenticação, autorização e gerenciamento de permissões baseadas em papéis (RBAC). Ideal para quem deseja explorar boas práticas em desenvolvimento de APIs modernas com Python.
</p>

<p align="center">
  <a href="#memo-sobre-o-projeto">Sobre o Projeto</a> •
  <a href="#rocket-tecnologias">Tecnologias</a> •
  <a href="#clipboard-requisitos">Requisitos</a> •
  <a href="#building_construction-arquitetura">Arquitetura</a> •
  <a href="#information_source-como-usar">Como Usar</a> •
  <a href="#handshake-como-contribuir">Como Contribuir</a> •
  <a href="#memo-licença">Licença</a>
</p>

---

## :memo: Sobre o Projeto

Este projeto é uma aplicação backend construída com **FastAPI**, projetada para gerenciar usuários, papéis, permissões e transações em um sistema baseado em **Role-Based Access Control (RBAC)**. A API suporta autenticação via JWT, autorização granular, auditoria de ações e integração com um banco de dados usando SQLAlchemy como ORM.

### Funcionalidades Principais
- **Autenticação**: Login de usuários com geração de tokens JWT.
- **Autor authorization**: Controle de acesso baseado em papéis e permissões.
- **Gerenciamento de Usuários**: Criação, atualização, listagem e exclusão de usuários.
- **Gestão de Papéis e Permissões**: Atribuição de papéis a usuários e permissões a papéis.
- **Auditoria**: Registro de informações de auditoria (usuário, IP, data de criação/atualização).
- **Testes Automatizados**: Suporte a testes com pytest e cobertura de código.

O projeto é estruturado para ser modular, escalável e seguir boas práticas de desenvolvimento, como separação de responsabilidades e uso de ferramentas modernas de desenvolvimento Python.

---

## :rocket: Tecnologias

Este projeto utiliza as seguintes tecnologias e ferramentas:

- **Linguagem**: [Python 3.11](https://www.python.org/)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Framework web para construção de APIs.
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Mapeamento objeto-relacional.
- **Banco de Dados**: [SQLite](https://sqlite.org/) - Banco de dados leve e embarcado.
- **Gerenciador de Dependências**: [Poetry](https://python-poetry.org/) - Gerenciamento de dependências e ambientes virtuais.
- **Migrações**: [Alembic](https://alembic.sqlalchemy.org/) - Gerenciamento de migrações de banco de dados.
- **Testes**: [pytest](https://pytest.org/) com [pytest-cov](https://pytest-cov.readthedocs.io/) para cobertura de testes.
- **Linting e Formatação**: [Ruff](https://github.com/charliermarsh/ruff), [Blue](https://blue.readthedocs.io/), e [isort](https://pycqa.github.io/isort/) para manter o código limpo.
- **Autenticação**: [python-jose](https://github.com/mpdavis/python-jose) para JWT e [bcrypt](https://pypi.org/project/bcrypt/) para hash de senhas.

---

## :clipboard: Requisitos

Para rodar ou contribuir com o projeto, você precisará das seguintes ferramentas instaladas:

| Ferramenta                                         | Versão       | Instalação (Linux/macOS)                     |
|----------------------------------------------------|--------------|----------------------------------------------|
| [Python](https://www.python.org/)                  | 3.11.9       | `asdf install python 3.11.9` ou similar      |
| [Poetry](https://python-poetry.org/)               | Latest       | `curl -sSL https://install.python-poetry.org | python3 -` |
| [Git](https://git-scm.com/)                        | Latest       | `sudo apt install git` (Linux) ou `brew install git` (macOS) |
| [SQLite](https://sqlite.org/)                      | Latest       | Geralmente pré-instalado, ou `sudo apt install sqlite3` |

**Nota**: Recomendamos o uso do `asdf` para gerenciar versões do Python. Consulte o arquivo `.tool-versions` para a versão exata do Python utilizada.

---

## :building_construction: Arquitetura

A estrutura do projeto é organizada para promover modularidade e facilitar a manutenção. Abaixo está a organização dos arquivos e diretórios:

```bash
FastAPI/
├── app/                        # Código-fonte principal da aplicação
│   ├── api/                    # Definição de rotas, controladores e esquemas
│   │   ├── assignment/         # Endpoints para designações (usuário-papel)
│   │   ├── authentication/     # Endpoints para autenticação (login, JWT)
│   │   ├── authorization/      # Endpoints para autorizações (papel-transação)
│   │   ├── role/               # Endpoints para gerenciamento de papéis
│   │   ├── transaction/        # Endpoints para gerenciamento de transações
│   │   ├── user/               # Endpoints para gerenciamento de usuários
│   ├── database/               # Configuração do banco de dados (SQLAlchemy)
│   ├── models/                 # Modelos ORM para as entidades do sistema
│   ├── utils/                  # Funções utilitárias (segurança, configurações, etc.)
│   ├── startup.py              # Inicialização da aplicação FastAPI
├── migrations/                 # Scripts de migração do banco de dados (Alembic)
├── seeds/                      # Scripts de seeds para a aplicação
├── tests/                      # Testes automatizados (pytest)
├── .secrets/                   # Arquivos sensíveis (ex.: SECURITY_API_SECRET_KEY)
├── .env-semple                 # Modelo para arquivo de configuração .env
├── alembic.ini                 # Configuração do Alembic
├── poetry.lock                 # Lockfile do Poetry com dependências fixas
├── pyproject.toml              # Configuração do projeto e dependências
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
├── .tool-versions              # Versões das ferramentas utilizadas
```

### Modelo de Dados
O projeto utiliza um modelo de dados baseado em RBAC, com as seguintes entidades principais:
- **User**: Representa os usuários do sistema.
- **Role**: Papéis que definem permissões.
- **Assignment**: Associa usuários a papéis.
- **Transaction**: Operações do sistema (ex.: criar, listar, excluir).
- **Authorization**: Associa papéis a transações, definindo permissões.

---

## :information_source: Como Usar

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/FastAPI.git
cd FastAPI
```

### 2. Configurar o Ambiente
Crie o arquivo `.env` baseado no modelo fornecido:
```bash
cp .env-semple .env
```

Edite o arquivo `.env` com as configurações adequadas. Exemplo:
```plaintext
DB_URL="sqlite:///database.db"
SECURITY_ALGORITHM="HS256"
SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Crie o diretório `.secrets` e adicione o arquivo `SECURITY_API_SECRET_KEY` com um valor seguro:
```bash
mkdir .secrets
echo "SUA_CHAVE_SECRETA_AQUI" > .secrets/SECURITY_API_SECRET_KEY
```

### 3. Instalar Dependências
Ative o ambiente virtual e instale as dependências com o Poetry:
```bash
poetry shell
poetry install
```

### 4. Aplicar Migrações
Execute as migrações para criar as tabelas no banco de dados:
A) aplique as migrations existentes:
```bash
alembic upgrade head
```
b) Suba os seedings de RBAC e de usuario admin
```bash
task setup_db
```

### 5. Executar a API
Inicie o servidor FastAPI com o comando:
```bash
task run
```

A API estará disponível em:
- **URL Local**: [http://localhost:8000](http://localhost:8000)
- **Documentação Interativa**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- **Documentação Alternativa**: [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc)

### 6. Executar Testes
Para rodar os testes automatizados e verificar a cobertura:
```bash
task test
```

O relatório de cobertura será gerado em `htmlcov/index.html`.

---

## :handshake: Como Contribuir

Adoramos contribuições! Se você deseja ajudar a melhorar este projeto, siga estas etapas:

### 1. Fork e Clone
Faça um fork do repositório e clone-o localmente:
```bash
git clone https://github.com/seu-usuario/FastAPI.git
cd FastAPI
```

### 2. Crie uma Branch
Crie uma branch para sua feature ou correção:
```bash
git checkout -b minha-feature
```

### 3. Siga as Convenções
- **Código**: Use o `ruff`, `blue` e `isort` para formatar o código (`task format`).
- **Commits**: Utilize mensagens de commit claras e siga o padrão do [Commitizen](https://commitizen-tools.github.io/commitizen/) (`cz commit`).
- **Testes**: Adicione testes para novas funcionalidades e garanta que `task test` passe.

### 4. Envie sua Contribuição
Faça o push da sua branch e crie um Pull Request:
```bash
git push origin minha-feature
```

No Pull Request, descreva claramente:
- O que foi feito.
- Por que a mudança é necessária.
- Como testar a alteração.

### Tarefas Disponíveis
- Adicionar novos endpoints para funcionalidades específicas.
- Melhorar a cobertura de testes.
- Implementar validações adicionais nos esquemas Pydantic.
- Adicionar suporte a outros bancos de dados (ex.: PostgreSQL).
- Criar documentação adicional ou exemplos de uso.

### Comandos Úteis
- **Formatar código**: `task format`
- **Verificar linting**: `task lint`
- **Executar testes**: `task test`
- **Gerar requirements.txt**: `task export_libs`

---

## :memo: Licença

Este projeto está licenciado sob a [MIT License](LICENSE). Veja o arquivo `LICENSE` para mais detalhes.

---

## :speech_balloon: Contato

Se tiver dúvidas ou sugestões, entre em contato:
- **Autores**: jvras <jvras58@gmail.com>
- **Issues**: [GitHub Issues](https://github.com/jvras58/FastAPI/issues)
