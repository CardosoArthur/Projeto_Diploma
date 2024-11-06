from flask import Flask, request, jsonify, render_template
import mysql.connector
import pika
import json
import time
import os

app = Flask(__name__)

# Configuração do caminho do template no diretório api
app.template_folder = "."

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

@app.route('/formulario', methods=['GET'])
def formulario():
    
    return render_template('formulario.html')

@app.route('/criar-diploma', methods=['POST'])
def criar_diploma():

    aluno_nome = request.form.get('aluno_nome')
    curso = request.form.get('curso')
    data_conclusao = request.form.get('data_conclusao')
    
    
    if not aluno_nome or not curso or not data_conclusao:
        return jsonify({'error': 'Por favor, preencha todos os campos'}), 400

    
    try:
        conn = mysql.connector.connect(
            database="diplomas", 
            user="arthur123", 
            password="123456", 
            host="database"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO certificados (nome, curso, data_conclusao) VALUES (%s, %s, %s)", 
                    (aluno_nome, curso, data_conclusao))
        conn.commit()
        
        
        diploma_id = cur.lastrowid
        
        # Envia o pedido para a fila
        channel.basic_publish(
            exchange='',
            routing_key='diploma_queue',
            body=json.dumps({
                'diploma_id': diploma_id,
                'aluno_nome': aluno_nome,
                'curso': curso,
                'data_conclusao': data_conclusao
            })
        )
        
        return jsonify({'status': 'Pedido enviado para processamento', 'diploma_id': diploma_id}), 201
    
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
