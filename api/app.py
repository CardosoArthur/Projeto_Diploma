from flask import Flask, request, jsonify
import psycopg2
import pika
import json

app = Flask(__name__)

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="diplomas", user="usuario", password="senha", host="database"
)
cur = conn.cursor()

# Configuração do RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='diploma_queue')

@app.route('/criar-diploma', methods=['POST'])
def criar_diploma():
    dados = request.json
    aluno_nome = dados['aluno_nome']
    curso = dados['curso']
    data_conclusao = dados['data_conclusao']
    
    # Insere os dados no banco
    cur.execute("INSERT INTO diplomas (aluno_nome, curso, data_conclusao) VALUES (%s, %s, %s) RETURNING id",
                (aluno_nome, curso, data_conclusao))
    diploma_id = cur.fetchone()[0]
    conn.commit()

    # Envia o pedido para a fila
    channel.basic_publish(exchange='',
                          routing_key='diploma_queue',
                          body=json.dumps({'diploma_id': diploma_id, 'aluno_nome': aluno_nome, 'curso': curso, 'data_conclusao': data_conclusao}))

    return jsonify({'status': 'Pedido enviado para processamento', 'diploma_id': diploma_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
