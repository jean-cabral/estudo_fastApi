# Dockerfile

# Usa imagem base do Python
FROM python:3.10-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
