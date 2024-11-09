
FROM python:3.9


RUN apt-get update && apt-get install -y wkhtmltopdf


WORKDIR /app


COPY requirements.txt .

# dependências do projeto
RUN pip install -r requirements.txt


COPY . .

# comando padrão para iniciar o Worker
CMD ["python", "worker.py"]
