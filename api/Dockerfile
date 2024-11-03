# Use uma imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para instalar as dependências
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Copie o restante do código da API para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta onde o serviço vai rodar (5000 é comum para APIs)
EXPOSE 5000

# Defina o comando padrão para iniciar a API
CMD ["python", "app.py"]
