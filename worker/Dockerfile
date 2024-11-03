# Use uma imagem base do Python
FROM python:3.9

# Instala wkhtmltopdf para geração de PDFs
RUN apt-get update && apt-get install -y wkhtmltopdf

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para instalar as dependências
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia o restante do código do Worker para o diretório de trabalho no contêiner
COPY . .

# Define o comando padrão para iniciar o Worker
CMD ["python", "worker.py"]
