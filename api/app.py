from flask import Flask, request, jsonify
import mysql.connector  # Troca psycopg2 por mysql.connector
import pika
import json

app = Flask(__name__)

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    database="diplomas", 
    user="usuario", 
    password="senha", 
    host="database"
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
    cur.execute("INSERT INTO diplomas (aluno_nome, curso, data_conclusao) VALUES (%s, %s, %s)", 
                (aluno_nome, curso, data_conclusao))
    conn.commit()
    
    # Recupera o ID do diploma recém-criado
    diploma_id = cur.lastrowid

    # Envia o pedido para a fila
    channel.basic_publish(exchange='',
                          routing_key='diploma_queue',
                          body=json.dumps({
                              'diploma_id': diploma_id, 
                              'aluno_nome': aluno_nome, 
                              'curso': curso, 
                              'data_conclusao': data_conclusao
                          }))

    return jsonify({'status': 'Pedido enviado para processamento', 'diploma_id': diploma_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
