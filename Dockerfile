# Etapa 1: imagem base com Python
FROM python:3.11-slim

# Etapa 2: diretório de trabalho dentro do container
WORKDIR /app

# Etapa 3: instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Etapa 4: copia o requirements.txt
COPY requirements.txt .

# Etapa 5: instala as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Etapa 6: copia o restante da aplicação
COPY . .

# Etapa 7: define a variável de ambiente para o Django
ENV PYTHONUNBUFFERED=1

# Etapa 8: executa as migrações e inicializa o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"]
