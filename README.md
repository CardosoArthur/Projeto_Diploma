
# Diploma Generator

Este projeto é um gerador de diplomas, projetado para automatizar a criação de certificados em formato PDF. Ele foi desenvolvido para facilitar a emissão de diplomas personalizados para alunos, participantes de cursos e outros eventos educacionais.

## Funcionalidades

- **Gerar diplomas em PDF**: permite a criação de certificados em formato PDF.
- **Personalização de conteúdo**: possibilita inserir o nome do aluno, curso e data no diploma.
- **Design personalizável**: o layout do diploma pode ser ajustado para se adequar à identidade visual da instituição.

## Estrutura do Projeto

- **api/**: Contém a aplicação principal que expõe uma API.
  - `app.py`: Script principal que define e executa a API.
  - `requirements.txt`: Arquivo com as dependências para a aplicação da API.

- **worker/**: Contém o código do "worker" responsável por processar tarefas assíncronas.
  - `worker.py`: Script principal do "worker".
  - `requirements.txt`: Arquivo com as dependências do "worker".
  - `Dockerfile`: Define o ambiente Docker para o "worker".

## Pré-requisitos

- **Docker**: Certifique-se de que o Docker está instalado para rodar os contêineres.
- **Python**: Caso deseje rodar localmente, instale as dependências do Python listadas nos arquivos `requirements.txt`.

## Executando o Projeto

### Usando Docker

1. **Inicie os containers:**:

   ```bash
    docker-compose up --build -d
   ```
- Ao preencher e enviar o formulário, uma pasta será criada no diretório do projeto contendo o PDF do diploma.
- Acesse a API no endereço: http://localhost:5000/formulario.

### Executando Localmente (Sem Docker)

1. **Instale as dependências**:
   - API:
     ```bash
     cd api
     pip install -r requirements.txt
     ```
   - Worker:
     ```bash
     cd worker
     pip install -r requirements.txt
     ```

2. **Execute os scripts**:
   - API:
     ```bash
     python app.py
     ```
   - Worker:
     ```bash
     python worker.py
     ```

## Licença

Este projeto está licenciado sob a licença MIT.

