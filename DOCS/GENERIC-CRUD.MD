## Controlador Generico (GenericController)

Este documento descreve como funciona o controlador generico de CRUD e como estender ou modificar o comportamento para validacoes e regras de negocio especificas, como no controller de usuario.

## Onde fica e qual o papel

- Implementacao: [app/utils/generic_controller.py](app/utils/generic_controller.py)
- Objetivo: prover operacoes CRUD comuns para qualquer model que herde de `AbstractBaseModel`.

O `GenericController` recebe o model no construtor e expõe metodos padrao:

- `get(db_session, obj_id)`
- `get_all(db_session, skip=0, limit=100, **kwargs)`
- `save(db_session, obj)`
- `update(db_session, obj)`
- `delete(db_session, obj_id)`

## Como funciona cada metodo

### get

Busca por ID usando `db_session.get`. Se nao achar, dispara `ObjectNotFoundException`.

### get_all

Permite busca com filtros e paginacao:

- `skip` e `limit` controlam a pagina
- `**kwargs` sao usados como filtros dinamicos
- campos `String` usam `ilike` com `%valor%`
- demais campos usam comparacao direta

Use este metodo quando quiser uma listagem simples com filtros basicos.

### save

Insere o objeto:

- `db_session.add` + `commit` + `refresh`
- em erro de integridade, faz `rollback` e levanta `IntegrityValidationException`

### update

Atualiza com base no `id` do objeto:

- valida se `obj.id` existe
- carrega a instancia atual via `get`
- atualiza atributos com `obj.as_dict()`
- `commit` + `refresh`
- em erro de integridade, faz `rollback` e levanta `IntegrityValidationException`

### delete

Remove por ID:

- carrega a instancia via `get`
- `delete` + `commit`

## Como estender e adicionar validacoes

A forma recomendada e criar um controller especifico que herda de `GenericController` e sobrescreve os metodos que precisam de regras extras. Exemplo real: `UserController`.

### Exemplo: UserController

Implementacao: [app/api/user/controller.py](app/api/user/controller.py)

O `UserController` sobrescreve `save` e `update` para hashear a senha antes de persistir:

```python
class UserController(GenericController):
	def __init__(self) -> None:
		super().__init__(User)

	def save(self, db_session: Session, obj: User) -> AbstractBaseModel:
		obj.password = get_password_hash(obj.password)
		return super().save(db_session, obj)

	def update(self, db_session: Session, obj: User) -> AbstractBaseModel:
		obj.password = get_password_hash(obj.password)
		return super().update(db_session, obj)
```

Esse padrao garante que a regra de negocio (hash de senha) sempre seja aplicada.

## Padroes recomendados para validacoes personalizadas

### 1) Validar antes de salvar

Use quando precisa bloquear dados invalidos antes de gravar:

```python
class ProductController(GenericController):
	def __init__(self) -> None:
		super().__init__(Product)

	def save(self, db_session: Session, obj: Product) -> AbstractBaseModel:
		if obj.price <= 0:
			raise ValueError("price must be greater than zero")
		return super().save(db_session, obj)
```

### 2) Enriquecer dados antes de salvar

Use quando precisa completar campos de auditoria ou derivados:

```python
class OrderController(GenericController):
	def __init__(self) -> None:
		super().__init__(Order)

	def save(self, db_session: Session, obj: Order) -> AbstractBaseModel:
		obj.total = sum(item.amount for item in obj.items)
		return super().save(db_session, obj)
```

### 3) Validar antes de atualizar

Use quando precisa impedir alteracoes proibidas:

```python
class RoleController(GenericController):
	def __init__(self) -> None:
		super().__init__(Role)

	def update(self, db_session: Session, obj: Role) -> AbstractBaseModel:
		if obj.name == "SUPER_ADMIN":
			raise ValueError("SUPER_ADMIN cannot be edited")
		return super().update(db_session, obj)
```

### 4) Filtrar resultados no get_all

Se voce precisa de filtros mais complexos (ex.: joins ou regras baseadas no usuario), substitua o `get_all`:

```python
class TransactionController(GenericController):
	def __init__(self) -> None:
		super().__init__(Transaction)

	def get_all(self, db_session: Session, skip: int = 0, limit: int = 100, **kwargs):
		query = (
			select(Transaction)
			.where(Transaction.is_active == True)
			.offset(skip)
			.limit(limit)
		)
		return list(db_session.scalars(query).all())
```

## Onde colocar regras de negocio

- Regras de persistencia e validacao: controller especifico (ex.: `UserController`).
- Regras de autorizacao: camada de autorizacao (ex.: `validate_transaction_access`).
- Validacoes de schema: Pydantic schemas em `app/api/<area>/schemas.py`.

## Boas praticas

- Mantenha o `GenericController` simples e generico.
- Adicione validacoes em controllers especificos.
- Prefira excecoes do dominio quando possivel (ex.: `IntegrityValidationException`).
- Evite duplicar logica de negocio nos routers.

## Checklist rapido para criar um novo controller

1. Criar controller e herdar de `GenericController`.
2. Passar o model correto no `super().__init__(Model)`.
3. Sobrescrever `save`, `update` ou `get_all` quando houver regra especial.
4. Usar o controller no router correspondente.
