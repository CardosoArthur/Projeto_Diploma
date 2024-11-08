import pdfkit
import pika
import mysql.connector  # Biblioteca de conexão MySQL
from jinja2 import Template
import json
import os
import time

# Função para tentar conexão ao RabbitMQ com retentativas
def connect_to_rabbitmq(retries=5, delay=5):
    for attempt in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            print("Connected to RabbitMQ on attempt", attempt + 1)
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to RabbitMQ after several attempts.")

# Conexão com o RabbitMQ
connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='diploma_queue')

# Função para conectar ao MySQL com retentativas
def connect_to_mysql(retries=5, delay=5):
    for attempt in range(retries):
        try:
            conn = mysql.connector.connect(
                database="diplomas",
                user="arthur123",
                password="123456",
                host="database"
            )
            print("Connected to MySQL on attempt", attempt + 1)
            return conn
        except mysql.connector.Error as e:
            print(f"MySQL connection attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to MySQL after several attempts.")

# Conexão com o banco de dados MySQL
conn = connect_to_mysql()
cur = conn.cursor()

# Função para buscar os dados do diploma no banco de dados
def get_diploma_data(diploma_id):
    query = "SELECT nome, nacionalidade, estado, data_nascimento, rg, data_conclusao, curso, carga_horaria FROM certificados WHERE id = %s"
    cur.execute(query, (diploma_id,))
    result = cur.fetchone()
    
    if result:
        keys = ["nome", "nacionalidade", "estado", "data_nascimento", "rg", "data_conclusao", "curso", "carga_horaria"]
        data = dict(zip(keys, result))
        return data
    else:
        print(f"Diploma com ID {diploma_id} não encontrado no banco de dados.")
        return None

# Função para carregar e renderizar o template com dados
def render_template(data):
    with open('template.html', 'r', encoding='utf-8') as file:
        template = Template(file.read())
        html_content = template.render(**data)
    return html_content

pdfkit_options = {
    'page-size': 'A4',
    'margin-top': '200mm',
    'margin-right': '10mm',
    'margin-bottom': '10mm',
    'margin-left': '10mm',
}

# Função para gerar e salvar o PDF
def generate_pdf(data, output_path='output/'):
    html_content = render_template(data)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    pdf_path = os.path.join(output_path, f"{data['nome']}_diploma.pdf")
    
    pdfkit.from_string(html_content, pdf_path)
    print(f"PDF gerado em: {pdf_path}")

# Função para processar mensagens do RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    diploma_id = message.get("id")
    print(f"ID do diploma recebido: {diploma_id}")
    
    # Buscar dados do diploma no banco de dados
    data = get_diploma_data(diploma_id)
    
    if data:
        # Gerar PDF usando os dados do banco de dados
        generate_pdf(data)
    else:
        print(f"Erro: Dados do diploma com ID {diploma_id} não encontrados.")

# Configuração para ouvir a fila do RabbitMQ
channel.basic_consume(queue='diploma_queue', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()
