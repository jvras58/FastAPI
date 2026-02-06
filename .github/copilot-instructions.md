## Objetivo

Este arquivo oferece instruções práticas e específicas para agentes de codificação automática que vão trabalhar neste repositório FastAPI. Foque em mudanças pequenas e bem justificadas; siga os padrões existentes.

## Visão geral da arquitetura

- Backend FastAPI modular em `app/` com rotas agrupadas por domínio em `app/api/*` (ex.: `authentication`, `user`, `role`, `transaction`, `assignment`, `authorization`). Veja `app/startup.py` para os prefixes e inclusão de routers.
- ORM: SQLAlchemy 2.x com modelos em `app/models/` e sessão gerada em `app/database/session.py` via `engine = create_engine(get_settings().DB_URL)` e `get_session()` (gerador).
- Migrações: Alembic (configurado em `alembic.ini`) e seeds em `seeds/` (`seed_super_user.py`, `seed_transactions.py`).

## Fluxos e pontos de integração importantes

- Autenticação JWT: utilitários em `app/utils/security.py` — funções principais: `create_access_token`, `extract_username`, `get_password_hash`, `verify_password`. O endpoint de token está em `app/api/authentication/router.py` (`POST /auth/token`).
- Dependência de sessão: use `SessionDep = Annotated[Session, Depends(get_session)]` quando precisar de acesso ao DB (padrão nos routers).
- Middleware de autorização: `app/api/authorization/middleware.py` — registra `X-Process-Time` e é adicionado em `startup.py`.

## Convenções de código e modelos

- Controllers: herdam de `app/utils/generic_controller.py`. Ex.: `app/api/user/controller.py` implementa `get_user_by_username`, `save` e `update` (hash de senha no `save`/`update`).
- Schemas/request/response: criá-los em `app/api/<area>/schemas.py` e usar `response_model=` nos routers. Ex.: `AccessToken` em `app/api/authentication/schemas.py`.
- Models usam `mapped_column` com nomes de coluna customizados (ex.: `username` mapeado para `str_username` em `app/models/user.py`). Atenção às diferenças entre atributo e nome físico da coluna.

## Como executar e testes (comandos já presentes)

- Uso de task runner `taskipy` (ver `pyproject.toml` -> [tool.taskipy.tasks]):
  - `task run` -> `uvicorn app.startup:app --host 0.0.0.0 --port 8000 --reload`
  - `task test` -> `pytest -s -x --cov=app -vv` (pré-tarefa: lint)
  - `task migrate` -> `alembic upgrade head`
  - `task setup_db` -> aplica migrations e roda seeds (`seed_transactions` e `seed_super_user`).

## Arquivos de configuração e segredos

- Variáveis: copie `.env-semple` para `.env` e preencha; segredo JWT esperado em `.secrets/SECURITY_API_SECRET_KEY` (crie `.secrets` localmente).
- `pyproject.toml` contém dependências e tarefas úteis; prefira esses comandos ao invés de inventar novos flows.

## Boas práticas específicas deste projeto

- Siga o padrão: adicionar schema -> controller -> router -> incluir em `app/startup.py` (com `prefix` e `tags`).
- Use `get_session()` (dependência) em endpoints para garantir o contexto de sessão correto.
- Para rotas autenticadas, use o provedor OAuth2 (`OAuth2PasswordBearer` em `app/api/authentication/controller.py`) e as funções de segurança existentes.
- Testes: ver `tests/` e factories em `tests/factory/`; use as fixtures definidas em `tests/conftest.py`.

## Exemplos rápidos (quando editar/implementar endpoints)

- Novo endpoint REST:
  1. criar `app/api/foo/schemas.py` (Pydantic models);
  2. criar `app/api/foo/controller.py` (opcional: herdar GenericController);
  3. criar `app/api/foo/router.py` com `APIRouter()` e dependências `SessionDep`;
  4. incluir no `app/startup.py`: `app.include_router(foo_router, prefix='/foo', tags=['Foo'])`.

## Onde procurar documentação de domínio

- RBAC e fluxos de autorização: `DOCS/PERMISSIONS.MD` e `DOCS/FLUXOGRAMA.MD`.
- README.MD tem informações de ambiente, devcontainer e processo de deploy.

## Avisos e limitações para agentes

- Não altere a forma de mapeamento das colunas sem ajustar migrations e seeds (models usam nomes físicos diferentes).
- Evite mudanças disruptivas no `pyproject.toml` sem coordenar dependências; prefira usar as tasks existentes para testes/execução.
- Assegure que as alterações em autenticação/segurança preservem o formato dos tokens (funções em `app/utils/security.py`).

---

Se algo aqui estiver incompleto ou você quiser que eu inclua snippets mais específicos (ex.: um template de `router.py`), diga o que prefere que eu adicione.
