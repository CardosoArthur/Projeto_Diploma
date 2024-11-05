import pdfkit
import pika
import mysql.connector  # Biblioteca de conexão MySQL
from jinja2 import Template
import json

# Configuração do RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    database="diplomas",
    user="usuario",
    password="senha",
    host="database"
)
cur = conn.cursor()

# Função para carregar e renderizar o template com dados
def render_template(data):
    with open('template_diploma.html', 'r', encoding='utf-8') as file:
        template = Template(file.read())
        html_content = template.render(
            nome=data['nome'],
            nacionalidade=data['nacionalidade'],
            estado=data['estado'],
            data_nascimento=data['data_nascimento'],
            documento=data['documento'],
            data_conclusao=data['data_conclusao'],
            curso=data['curso'],
            carga_horaria=data['carga_horaria'],
            data_emissao=data['data_emissao'],
            nome_assinatura=data['nome_assinatura'],
            cargo=data['cargo']
        )
    return html_content

# Função para processar mensagens da fila
def callback(ch, method, properties, body):
    dados = json.loads(body)
    diploma_id = dados['diploma_id']
    
    # Renderizar o template HTML com os dados do diploma
    html_content = render_template(dados)

    # Gerar PDF a partir do HTML renderizado
    pdf = pdfkit.from_string(html_content, False)

    # Atualizar o banco de dados com o PDF gerado
    query = "UPDATE diplomas SET pdf = %s WHERE id = %s"
    cur.execute(query, (pdf, diploma_id))
    conn.commit()

    print("Diploma gerado e salvo no banco")

# Escutar a fila de diplomas
channel.basic_consume(queue='diploma_queue', on_message_callback=callback, auto_ack=True)
print("Worker aguardando mensagens...")
channel.start_consuming()
