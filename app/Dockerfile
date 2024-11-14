# Use uma imagem base com Python
FROM python:3.13-alpine

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Defina o comando padrão
CMD ["python", "app.py"]
