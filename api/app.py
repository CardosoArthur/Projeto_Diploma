from flask import Flask, request, jsonify, render_template
import mysql.connector
import pika
import json
import os

app = Flask(__name__)

# Configuração do caminho do template no diretório api
app.template_folder = "."

# Configuração do RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='diploma_queue')

@app.route('/formulario', methods=['GET'])
def formulario():
    # Renderiza o formulário HTML existente em api/formulario.html
    return render_template('api/formulario.html')

@app.route('/criar-diploma', methods=['POST'])
def criar_diploma():
    # Captura dados do formulário
    aluno_nome = request.form.get('aluno_nome')
    curso = request.form.get('curso')
    data_conclusao = request.form.get('data_conclusao')
    
    # Valida se todos os dados foram preenchidos
    if not aluno_nome or not curso or not data_conclusao:
        return jsonify({'error': 'Por favor, preencha todos os campos'}), 400

    # Insere os dados no banco de dados
    try:
        conn = mysql.connector.connect(
            database="diplomas", 
            user="usuario", 
            password="senha", 
            host="database"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO diplomas (aluno_nome, curso, data_conclusao) VALUES (%s, %s, %s)", 
                    (aluno_nome, curso, data_conclusao))
        conn.commit()
        
        # Recupera o ID do diploma recém-criado
        diploma_id = cur.lastrowid
        
        # Envia o pedido para a fila RabbitMQ
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
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
