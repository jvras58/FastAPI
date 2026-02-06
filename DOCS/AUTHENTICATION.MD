# 🔐 **SISTEMA DE AUTENTICAÇÃO - GUIA COMPLETO**

## 📋 **VISÃO GERAL**

Este projeto utiliza um sistema de autenticação robusto baseado em **JWT (JSON Web Tokens)** para garantir a segurança das operações da API. O sistema trabalha em conjunto com o modelo **RBAC (Role-Based Access Control)** para fornecer controle granular de acesso.

### **Componentes Principais**
- **JWT Tokens**: Tokens de acesso para autenticação de usuários
- **BCrypt**: Hash seguro de senhas
- **OAuth2**: Padrão de autenticação com senha
- **python-jose**: Biblioteca para geração e validação de tokens JWT

---

## 🔄 **FLUXO DE AUTENTICAÇÃO**

```mermaid
sequenceDiagram
    participant Cliente
    participant API
    participant DB
    participant JWT
    
    Cliente->>API: POST /auth/token (username, password)
    API->>DB: Buscar usuário por username
    DB-->>API: Retorna dados do usuário
    API->>API: Verificar senha (bcrypt)
    API->>JWT: Gerar token JWT
    JWT-->>API: Token gerado
    API-->>Cliente: {access_token, token_type}
    
    Cliente->>API: GET /users/me (Authorization: Bearer token)
    API->>JWT: Validar e decodificar token
    JWT-->>API: Dados do usuário extraídos
    API->>DB: Buscar usuário completo
    DB-->>API: Dados do usuário
    API-->>Cliente: Informações do usuário
```

---

## 🚀 **OBTENDO UM TOKEN DE ACESSO**

### **1. Endpoint de Login**

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=senha123
```

### **2. Usando cURL**

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=senha123"
```

### **3. Resposta Bem-Sucedida**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **4. Possíveis Erros**

| Código | Descrição | Motivo |
|--------|-----------|--------|
| 400 | Bad Request | Credenciais incorretas (usuário ou senha inválidos) |
| 422 | Unprocessable Entity | Formato de requisição inválido |

---

## 🔑 **ESTRUTURA DO TOKEN JWT**

### **Cabeçalho (Header)**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### **Payload (Dados)**
```json
{
  "sub": "nome_usuario",
  "exp": 1234567890,
  "nbf": 1234567890,
  "iat": 1234567890,
  "iss": "FA-Backend"
}
```

### **Campos do Payload**
| Campo | Descrição |
|-------|-----------|
| `sub` | Subject - Nome de usuário (username) |
| `exp` | Expiration Time - Data/hora de expiração do token |
| `nbf` | Not Before - Data/hora antes da qual o token não é válido |
| `iat` | Issued At - Data/hora em que o token foi emitido |
| `iss` | Issuer - Emissor do token (FA-Backend) |

### **Configurações de Tempo**
- **Validade do Token**: Configurável via `SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES` (padrão: 30 minutos)
- **Algoritmo**: HS256 (configurável via `SECURITY_ALGORITHM`)
- **Chave Secreta**: Armazenada em `.secrets/SECURITY_API_SECRET_KEY`

---

## 🔒 **USANDO TOKENS NAS REQUISIÇÕES**

### **1. Incluir Token no Cabeçalho**

```http
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **2. Exemplo com cURL**

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### **3. Exemplo com Python (requests)**

```python
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "http://localhost:8000/users/me",
    headers=headers
)
```

### **4. Exemplo com JavaScript (fetch)**

```javascript
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";

fetch("http://localhost:8000/users/me", {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🛡️ **SEGURANÇA DE SENHAS**

### **Hash de Senhas com BCrypt**

O sistema utiliza **BCrypt** para armazenar senhas de forma segura:

1. **Criação de Senha**:
   - Senha em texto plano é recebida
   - Salt aleatório é gerado
   - Senha é hasheada com o salt
   - Hash é armazenado no banco de dados

2. **Verificação de Senha**:
   - Usuário envia senha em texto plano
   - Sistema busca hash armazenado
   - BCrypt compara senha com hash
   - Retorna verdadeiro ou falso

### **Funções de Segurança**

#### `get_password_hash(password: str) -> str`
```python
# Uso: Ao criar ou atualizar senha de usuário
hashed = get_password_hash("senha_do_usuario")
# Retorna: "$2b$12$KIXxH9e7..."
```

#### `verify_password(plain_password: str, hashed_password: str) -> bool`
```python
# Uso: Ao validar login
is_valid = verify_password("senha_do_usuario", hashed_from_db)
# Retorna: True ou False
```

#### `create_access_token(data: dict) -> str`
```python
# Uso: Ao gerar token após login bem-sucedido
token = create_access_token({"sub": "nome_usuario"})
# Retorna: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### `extract_username(jwt_token: str) -> str`
```python
# Uso: Ao validar token e extrair usuário
username = extract_username(token)
# Retorna: "nome_usuario"
```

---

## 👤 **OBTENDO O USUÁRIO ATUAL**

### **Dependência FastAPI**

O sistema fornece uma dependência `get_current_user` para obter o usuário autenticado:

```python
from app.api.authentication.controller import get_current_user
from app.models.user import User
from fastapi import Depends

@router.get("/protected-route")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"username": current_user.username}
```

### **Processo de Validação**

1. **Extração do Token**: Token é extraído do cabeçalho `Authorization`
2. **Decodificação JWT**: Token é decodificado e validado
3. **Extração do Username**: Campo `sub` do payload é extraído
4. **Busca no Banco**: Usuário é buscado no banco de dados
5. **Retorno**: Objeto `User` completo é retornado

### **Exceções Possíveis**

| Exceção | Código HTTP | Quando Ocorre |
|---------|-------------|---------------|
| `CredentialsValidationException` | 401 | Token inválido, expirado ou usuário não encontrado |
| `IncorrectCredentialException` | 400 | Username ou senha incorretos no login |

---

## 🔗 **INTEGRAÇÃO COM RBAC**

### **Fluxo Completo: Autenticação + Autorização**

```
1. Login (Autenticação)
   ↓
2. Token JWT Gerado
   ↓
3. Token em Requisição Protegida
   ↓
4. Validar Token → Obter Usuário
   ↓
5. Validar Permissão (RBAC)
   ↓
6. Executar Operação ou Negar Acesso
```

### **Validação de Permissões**

```python
from app.api.authorization.controller import validate_transaction_access
from app.api.authentication.controller import get_current_user

@router.post("/users/create")
async def create_user(
    db_session: Session,
    current_user: User = Depends(get_current_user)
):
    # Valida se usuário tem permissão para criar usuários
    validate_transaction_access(
        db_session, 
        current_user, 
        'OP_1040001'  # Código da operação "User - Create"
    )
    
    # Usuário tem permissão, executar operação...
```

### **Cadeia de Validação RBAC**

```
Token JWT → User → Assignment → Role → Authorization → Transaction
```

Para mais detalhes sobre o sistema RBAC, consulte [PERMISSIONS.MD](PERMISSIONS.MD).

---

## 📝 **CENÁRIOS PRÁTICOS**

### **Cenário 1: Login e Acesso a Recurso Protegido**

```bash
# 1. Fazer login e obter token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=senha123" \
  | jq -r '.access_token')

# 2. Usar token para acessar recurso protegido
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer $TOKEN"
```

### **Cenário 2: Token Expirado**

```bash
# Após 30 minutos (ou tempo configurado), o token expira
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer TOKEN_EXPIRADO"

# Resposta:
# HTTP 401 Unauthorized
# {"detail": "Could not validate credentials"}

# Solução: Fazer novo login e obter novo token
```

### **Cenário 3: Criação de Usuário Sem Autenticação**

```bash
# Este é o ÚNICO endpoint que não requer autenticação
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novo_usuario",
    "display_name": "Novo Usuário",
    "email": "novo@email.com",
    "password": "senha123"
  }'

# ⚠️ IMPORTANTE: Usuário criado não tem nenhuma permissão
# Um admin precisa atribuir um Role via Assignment
```

### **Cenário 4: Tentativa de Acesso Sem Token**

```bash
curl -X GET "http://localhost:8000/users/"

# Resposta:
# HTTP 401 Unauthorized
# {"detail": "Not authenticated"}
```

---

## ⚙️ **CONFIGURAÇÃO DO SISTEMA**

### **Variáveis de Ambiente (.env)**

```plaintext
# Algoritmo de criptografia JWT
SECURITY_ALGORITHM=HS256

# Tempo de expiração do token em minutos
SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES=30

# URL do banco de dados
DB_URL=sqlite:///database.db
```

### **Chave Secreta (.secrets/SECURITY_API_SECRET_KEY)**

```bash
# Gerar chave secreta forte
openssl rand -hex 32 > .secrets/SECURITY_API_SECRET_KEY

# Ou usar Python
python -c "import secrets; print(secrets.token_hex(32))" > .secrets/SECURITY_API_SECRET_KEY
```

⚠️ **IMPORTANTE**: 
- NUNCA commite a chave secreta no repositório
- Use uma chave diferente para produção
- Mantenha a chave em local seguro

---

## 🔍 **ARQUITETURA DO CÓDIGO**

### **Estrutura de Arquivos**

```
app/api/authentication/
├── router.py          # Endpoint de login (/auth/token)
├── controller.py      # Lógica de autenticação (login, validação)
└── schemas.py         # Modelos Pydantic (AccessToken, TokenData)

app/utils/
├── security.py        # Funções de segurança (JWT, hash)
└── settings.py        # Configurações da aplicação
```

### **Fluxo de Código**

1. **Router** (`router.py`):
   - Define endpoint `/auth/token`
   - Recebe credenciais via `OAuth2PasswordRequestForm`
   - Chama controller para processar login

2. **Controller** (`controller.py`):
   - `execute_user_login()`: Valida credenciais e gera token
   - `get_current_user()`: Extrai e valida usuário do token
   - Usa funções de `security.py` para operações criptográficas

3. **Security** (`security.py`):
   - `create_access_token()`: Gera token JWT
   - `verify_password()`: Valida senha com bcrypt
   - `get_password_hash()`: Hash de senha para armazenamento
   - `extract_username()`: Extrai username do token

---

## 🧪 **TESTANDO O SISTEMA**

### **Teste Manual via Swagger UI**

1. Acesse: http://localhost:8000/api/v1/docs
2. Vá até o endpoint `/auth/token`
3. Clique em "Try it out"
4. Preencha username e password
5. Clique em "Execute"
6. Copie o `access_token` retornado
7. Clique no botão "Authorize" (cadeado) no topo da página
8. Cole o token no campo "Value"
9. Clique em "Authorize"
10. Agora você pode testar endpoints protegidos

### **Teste com pytest**

```bash
# Executar todos os testes
pytest tests/

# Executar testes de autenticação específicos
pytest tests/ -k "auth"

# Com cobertura
pytest --cov=app tests/
```

---

## 🚨 **SEGURANÇA E BOAS PRÁTICAS**

### ✅ **O Sistema Implementa**
- Hash seguro de senhas com BCrypt e salt aleatório
- Tokens JWT com expiração configurável
- Validação de token em toda requisição protegida
- Chave secreta armazenada fora do código
- OAuth2 password flow padrão
- Timestamps completos em tokens (iat, nbf, exp)

### ⚠️ **Recomendações**
- Use HTTPS em produção (nunca HTTP)
- Rotacione a chave secreta periodicamente
- Configure tempo de expiração adequado (nem muito curto, nem muito longo)
- Implemente refresh tokens para melhor experiência do usuário
- Use rate limiting para prevenir ataques de força bruta
- Monitore tentativas de login falhadas
- Implemente logout do lado do servidor (blacklist de tokens)

### 🛡️ **Proteções Contra Ataques**
- **Força Bruta**: Senhas hasheadas com BCrypt (lento por design)
- **Token Replay**: Tokens expiram após tempo configurado
- **Token Forgery**: Assinatura HMAC-SHA256 com chave secreta
- **SQL Injection**: SQLAlchemy ORM com queries parametrizadas
- **XSS**: FastAPI serializa automaticamente respostas JSON

---

## 📚 **REFERÊNCIAS**

### **Documentação Relacionada**
- [PERMISSIONS.MD](PERMISSIONS.MD) - Sistema de permissões RBAC
- [FLUXOGRAMA.MD](FLUXOGRAMA.MD) - Fluxo geral da aplicação
- [README.MD](../README.MD) - Documentação principal do projeto

### **Bibliotecas Utilizadas**
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [python-jose](https://python-jose.readthedocs.io/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [OAuth2 Specification](https://oauth.net/2/)
- [JWT.io](https://jwt.io/) - Decoder de tokens JWT

### **Especificações**
- [RFC 7519 - JWT](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 6749 - OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749)
- [BCrypt Algorithm](https://en.wikipedia.org/wiki/Bcrypt)

---

## 💡 **PERGUNTAS FREQUENTES**

### **1. Quanto tempo o token dura?**
Por padrão, 30 minutos. Configurável via `SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES` no `.env`.

### **2. O que acontece quando o token expira?**
O usuário recebe um erro 401 e precisa fazer login novamente para obter um novo token.

### **3. Posso ter múltiplos tokens ativos?**
Sim, cada login gera um novo token. Todos permanecem válidos até expirarem.

### **4. Como faço logout?**
Atualmente, o logout é feito no lado do cliente (descartando o token). Para logout do servidor, seria necessário implementar uma blacklist de tokens.

### **5. Posso renovar um token sem fazer login novamente?**
Não, atualmente. Para implementar isso, seria necessário adicionar refresh tokens ao sistema.

### **6. Qual a diferença entre autenticação e autorização?**
- **Autenticação**: Verifica QUEM você é (login com usuário/senha, validação de token)
- **Autorização**: Verifica O QUE você pode fazer (permissões via RBAC)

### **7. Por que BCrypt ao invés de SHA256?**
BCrypt é especificamente projetado para senhas, sendo intencionalmente lento para dificultar ataques de força bruta, além de incluir salt automaticamente.

### **8. O token pode ser decodificado por qualquer um?**
O token pode ser decodificado (payload é base64), mas não pode ser MODIFICADO sem a chave secreta. A assinatura garante que o token não foi adulterado.

---

## 📞 **SUPORTE**

Para dúvidas ou problemas com autenticação:
- Abra uma issue no GitHub
- Consulte a documentação do FastAPI
- Revise os logs da aplicação
- Verifique as configurações do `.env` e `.secrets`

---

**Última atualização**: Dezembro 2024  
**Versão da Documentação**: 1.0
