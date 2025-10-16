#!/bin/bash
set -e

echo "🚀 Starting FastAPI CrewAI Application..."

# Função para aguardar o PostgreSQL (se estiver usando PostgreSQL)
wait_for_postgres() {
    if [[ "$DB_URL" == *"postgresql"* ]]; then
        echo "⏳ Waiting for PostgreSQL to be ready..."

        # Extrair host e porta do DB_URL
        # Format: postgresql://user:pass@host:port/db
        DB_HOST=$(echo "$DB_URL" | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo "$DB_URL" | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

        # Valores padrão se não encontrados
        DB_HOST=${DB_HOST:-postgres}
        DB_PORT=${DB_PORT:-5432}

        echo "Verificando conexão com $DB_HOST:$DB_PORT..."

        # Aguarde até que a porta esteja disponível usando netcat ou timeout
        for i in {1..30}; do
            if timeout 1 bash -c "</dev/tcp/$DB_HOST/$DB_PORT" 2>/dev/null; then
                echo "✅ PostgreSQL está pronto!"
                return 0
            fi
            echo "❌ PostgreSQL ainda não está pronto (tentativa $i/30)..."
            sleep 2
        done

        echo "💥 PostgreSQL não ficou pronto a tempo"
        exit 1
    else
        echo "📁 Usando banco de dados SQLite - verificação de conexão não necessária"
    fi
}

# Aguarde o banco de dados, se necessário
wait_for_postgres

# Execute as migrações do banco de dados
echo "🔄 Executando migrações do banco de dados..."
alembic upgrade head

echo "✅ Migrações concluídas com sucesso!"

# Inicie a aplicação FastAPI com Uvicorn
echo "🌟 Iniciando a aplicação FastAPI com uvicorn..."
exec uvicorn app.startup:app --host 0.0.0.0 --port 8000 --workers 4
