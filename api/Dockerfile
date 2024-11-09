
FROM python:3.9

# diretório de trabalho dentro do contêiner
WORKDIR /app

# arquivo de requisitos com as dependências
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install -r requirements.txt


COPY . .

# porta onde o serviço vai rodar
EXPOSE 5000

# comando padrão para iniciar a API
CMD ["python", "app.py"]
