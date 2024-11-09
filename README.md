Este projeto é uma aplicação para geração de certificados em PDF, a partir dos dados preenchidos em um formulário, composta por uma API, um banco de dados e um worker, gerenciados pelo Docker Compose.

Estrutura do Projeto
api/: Contém a API do projeto, incluindo rotas, modelos e a lógica de negócio.
db/: Diretório dedicado ao banco de dados, que pode conter scripts de inicialização e configuração.
worker/: Módulo para processos de background e tarefas assíncronas, integrados com a API ou banco de dados.
output/: Diretório de armazenamento de arquivos de saída, como logs ou PDFs gerados.
docker-compose.yml: Arquivo de configuração do Docker Compose, usado para orquestração dos serviços.
Requisitos
Docker e Docker Compose instalados.
Configurações específicas para a API ou banco de dados, conforme necessário.
Configuração e Instalação
Clone o repositório:

bash
Copiar código
git clone <URL_DO_REPOSITORIO>
Navegue até o diretório do projeto:

bash
Copiar código
cd GS
Inicie os serviços usando o Docker Compose:

bash
Copiar código
docker-compose up -d
Uso
Acesse a API no endereço: http://localhost:5000/formulario.
Para visualizar logs e saídas geradas, consulte o diretório output.
