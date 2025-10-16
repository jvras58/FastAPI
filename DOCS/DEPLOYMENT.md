# FastAPI CrewAI - Deployment em Produção

## Pré-requisitos

- Docker
- Docker Compose
- Uma chave da API do GROQ

## Setup de Produção

1. **Clone o repositório e navegue até a pasta:**
   ```bash
   cd fastapi-crewai
   ```

2. **Crie o arquivo de variáveis de ambiente:**
   ```bash
   cp .env-prod.example .env.prod
   ```

3. **Edite o arquivo `.env.prod` com suas configurações:**
   ```bash
   nano .env.prod
   ```
   
   Certifique-se de atualizar:
   - `GROQ_API_KEY`: Sua chave da API do GROQ
   - Opcionalmente, as credenciais do PostgreSQL se desejar alterá-las

4. **Inicie os serviços:**
   ```bash
   # Build e start dos containers
   docker compose up -d --build

   # Ou se você quiser ver os logs
   docker compose up --build
   ```

5. **Verifique se tudo está funcionando:**
   ```bash
   # Verificar status dos containers
   docker compose ps

   # Verificar logs da aplicação
   docker compose logs app

   # Verificar logs do PostgreSQL
   docker compose logs postgres
   ```

6. **Acesse a aplicação:**
   - API: http://localhost:8000
   - Documentação Swagger: http://localhost:8000/api/v1/docs
   - Redoc: http://localhost:8000/api/v1/redoc

## Comandos Úteis

### Gerenciamento dos Containers

```bash
# Parar os serviços
docker compose down

# Parar e remover volumes (CUIDADO: isso remove os dados do banco!)
docker compose down -v

# Rebuild da aplicação após mudanças no código
docker compose up -d --build app

# Ver logs em tempo real
docker compose logs -f app
```

### Gerenciamento do Banco de Dados

```bash
# Executar migrations manualmente
docker compose exec app alembic upgrade head

# Acessar o PostgreSQL diretamente
docker compose exec postgres psql -U fastapi_user -d fastapi_crewai

# Backup do banco
docker compose exec postgres pg_dump -U fastapi_user fastapi_crewai > backup.sql

# Restaurar backup
docker compose exec -T postgres psql -U fastapi_user -d fastapi_crewai < backup.sql
```

## Estrutura dos Serviços

### PostgreSQL
- **Imagem:** postgres:16-alpine
- **Porta:** 5432
- **Volume:** postgres_data (persistente)
- **Health Check:** Configurado para garantir que está pronto antes da app iniciar

### FastAPI App
- **Build:** Dockerfile local (baseado no exemplo da [documentação do uv astral](https://github.com/astral-sh/uv-docker-example))
- **Porta:** 8000
- **Workers:** 4 (uvicorn)
- **Dependências:** Aguarda o PostgreSQL estar healthy
- **Auto-migrations:** Executa `alembic upgrade head` automaticamente no startup

## Considerações de Produção

1. **Segurança:**
   - Altere as credenciais padrão do PostgreSQL
   - Use secrets do Docker Swarm ou Kubernetes para senhas em produção real
   - Configure HTTPS com reverse proxy (nginx, traefik)

2. **Performance:**
   - Ajuste o número de workers do uvicorn conforme necessário
   - Configure limites de recursos nos containers
   - Use um proxy reverso para servir arquivos estáticos

3. **Monitoramento:**
   - Configure logs estruturados
   - Adicione health checks customizados
   - Configure alertas para falhas

4. **Backup:**
   - Configure backups automáticos do PostgreSQL
   - Teste a restauração regularmente

## Troubleshooting

### App não conecta ao banco
- Verifique se o PostgreSQL está healthy: `docker compose logs postgres`
- Confirme a DB_URL no compose.yml

### Migrations falham
- Execute manualmente: `docker compose exec app alembic upgrade head`
- Verifique logs: `docker compose logs app`

### Performance baixa
- Monitore recursos: `docker stats`
- Ajuste número de workers no compose.yml
- Considere usar um load balancer
