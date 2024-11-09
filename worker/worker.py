import pdfkit
import pika
import mysql.connector  
from jinja2 import Template
import json
import os
import time


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


connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='diploma_queue')


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


conn = connect_to_mysql()
cur = conn.cursor()


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


def render_template(data):
    with open('template.html', 'r', encoding='utf-8') as file:
        template = Template(file.read())
        html_content = template.render(**data)
    return html_content

pdfkit_options = {
    'page-size': 'A4',
    'margin-top': '10mm',
    'margin-right': '10mm',
    'margin-bottom': '10mm',
    'margin-left': '10mm',
    'zoom': 1.0  


def generate_pdf(data, output_path='output/'):
    html_content = render_template(data)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    pdf_path = os.path.join(output_path, f"{data['nome']}_diploma.pdf")
    
    pdfkit.from_string(html_content, pdf_path)
    print(f"PDF gerado em: {pdf_path}")


def callback(ch, method, properties, body):
    message = json.loads(body)
    diploma_id = message.get("id")
    print(f"ID do diploma recebido: {diploma_id}")
    
    data = get_diploma_data(diploma_id)
    
    if data:
        
        generate_pdf(data)
    else:
        print(f"Erro: Dados do diploma com ID {diploma_id} não encontrados.")


channel.basic_consume(queue='diploma_queue', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()
