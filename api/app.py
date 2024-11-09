from flask import Flask, request, jsonify, render_template
import mysql.connector
import pika
import json
import time
import os

app = Flask(__name__)


app.template_folder = "."

# conexão ao RabbitMQ com retentativas
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
    
    # Receber dados do formulário
    aluno_nome = request.form.get('aluno_nome')
    nacionalidade = request.form.get('nacionalidade')
    estado = request.form.get('estado')
    data_nascimento = request.form.get('data_nascimento')
    rg = request.form.get('rg')
    data_conclusao = request.form.get('data_conclusao')
    curso = request.form.get('curso')
    carga_horaria = request.form.get('carga_horaria')
    data_emissao = request.form.get('data_emissao')
    
    if not aluno_nome or not curso or not data_conclusao:
        return jsonify({'error': 'Por favor, preencha todos os campos'}), 400

    try:
        # Conectar ao banco de dados e inserir dados
        conn = mysql.connector.connect(
            database="diplomas", 
            user="arthur123", 
            password="123456", 
            host="database"
        )
        cur = conn.cursor()
        query = """
        INSERT INTO certificados (nome, nacionalidade, estado, data_nascimento, rg, data_conclusao, curso, carga_horaria, data_emissao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (aluno_nome, nacionalidade, estado, data_nascimento, rg, data_conclusao, curso, carga_horaria, data_emissao)
        cur.execute(query, values)
        conn.commit()
        
        diploma_id = cur.lastrowid
        
        # Enviar apenas o diploma_id para a fila do RabbitMQ
        channel.basic_publish(
            exchange='',
            routing_key='diploma_queue',
            body=json.dumps({'id': diploma_id})
        )   
        
        return jsonify({'status': 'Informações inseridas no banco de dados', 'diploma_id': diploma_id}), 201
    
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
