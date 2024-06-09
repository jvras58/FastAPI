<h1 align="center">
  <a href="#">Projeto de Estudos com FASTAPI</a>
</h1>

<p align="center">
  <a href="#memo-requisitos">Requisitos</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#rocket-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#information_source-como-usar">Como usar</a>
</p>

## :memo: Requisitos

| Ferramenta                                         | Versão  | Descrição                                   |
| -------------------------------------------------- | ------- | ------------------------------------------- |
| [Poetry](https://python-poetry.org/)               | -       | gerenciador dependências em projetos Python |
| [Python](https://www.python.org/)                  | -       | Linguagem de desenvolvimento                |
| [Git](https://git-scm.com)                         | -       | Controle de versões                         |
| [SQLite](https://sqlite.org/)                      | -       | Sistema de gerenciamento de banco de dados  |


## :rocket: Tecnologias

Este projeto está sendo desenvolvido com:

- Gerenciador: [Poetry](https://python-poetry.org/)
- Linguagem e ambiente: [Python](https://www.python.org/)
- Object-Relation-Mapper (ORM): [SQLAlchemy](https://www.sqlalchemy.org/)
- Banco de dados: [SQLite](https://sqlite.org/)


## :information_source: Como usar

```bash
# Clonar este repositório
$ git clone git@github.com:jvras58/back-fastapi.git

# Ir para o repositório
$ cd back-fastapi  

# Criar o arquivo .env com os valores adequados ao ambiente. pasta .secrets precisa ter (TESTE_SECRET).
$ cp .env-semple .env

# Entre no ambiente virtual
$ poetry shell

# Instalar as dependências
$ poetry install

# Executar as migrations
  $ alembic upgrade head

# Executar a api
$ task run
```

- Endereço local: (http://localhost:8000)


---
