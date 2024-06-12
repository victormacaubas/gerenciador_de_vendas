# Sistema de E-commerce

## Contexto
Este é um sistema de e-commerce para a venda de produtos diversos. O sistema foi desenvolvido com base nos seguintes requisitos:

- O sistema deve ser criado de acordo com o modelo descrito abaixo;
- O sistema deve permitir a criação e a destruição completa do banco de dados;
- O sistema deve possuir 20 produtos, 5 cargos e 100 clientes nativos;
- O sistema deve possuir a opção de cadastrar apenas produtos e clientes.

## Tecnologias Utilizadas

### Django
Django é um framework de desenvolvimento web de alto nível, escrito em Python, que incentiva o desenvolvimento rápido e o design limpo e pragmático. Com Django, os desenvolvedores podem criar aplicativos web seguros e escaláveis de maneira eficiente. Algumas características do Django incluem:

- **Administração Automática**: Django fornece uma interface administrativa pronta para uso, facilitando a gestão dos dados.
- **Segurança**: Django ajuda os desenvolvedores a evitar muitas falhas de segurança comuns por padrão.
- **Escalabilidade**: Django é usado por muitos sites de alto tráfego, como Instagram e Pinterest, demonstrando sua capacidade de lidar com grande escala.

## Funcionalidades do Sistema

1. **Criação e Destruição do Banco de Dados**
    - Comandos disponíveis para criar e destruir completamente o banco de dados, facilitando a administração e manutenção do sistema.

2. **Cadastro de Produtos e Clientes**
    - Possibilidade de cadastrar novos produtos e clientes através da interface administrativa fornecida pelo Django.

3. **População Inicial do Banco de Dados**
    - O sistema vem com 20 produtos, 5 cargos e 100 clientes já cadastrados para facilitar o início da utilização.

## Como Executar o Projeto

## Pré-requisitos

- Docker
- Docker Compose

## Como executar a aplicação

Siga os passos abaixo para configurar e executar a aplicação:

1. **Clone o repositório**

   ```sh
   git clone https://github.com/victormacaubas/gerenciador_de_vendas.git
   cd gerenciador_de_vendas
   ```

2. **Configure o arquivo `.env`**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

   ```env
   MYSQL_ROOT_PASSWORD=sua_senha_de_root
   DB_NAME=nome_do_banco
   DB_USER=usuario_do_banco
   DB_PASSWORD=senha_do_banco
   DB_HOST=db
   DB_PORT=3306

   # Senhas adicionais
   GERENTE_PASSWORD=sua_senha_de_gerente
   FUNCIONARIO_PASSWORD=sua_senha_de_funcionario
   SUPERUSER_PASSWORD=sua_senha_de_superuser
   ```

3. **Construa e execute os contêineres**

   No root do projeto, execute o seguinte comando para construir e iniciar os contêineres Docker:

   ```sh
   docker-compose up --build
   ```

4. **Rode as migrações**

   Após os contêineres serem iniciados, abra outro terminal e execute o seguinte comando para rodar as migrações do banco de dados:

   ```sh
   docker-compose exec web python manage.py makemigrations vendas_app
   docker-compose exec web python manage.py migrate
   ```

5. **Acesse a aplicação**

   Após rodar as migrações, você pode acessar a aplicação através do seu navegador no endereço:

   ```
   http://localhost:1337
   ```

## Comandos Úteis

- **Parar os contêineres**

  ```sh
  docker-compose down
  ```

- **Acessar o shell do contêiner web**

  ```sh
  docker-compose exec web sh
  ```

- **Deleter o Banco**

  ```sh
   docker-compose exec web python manage.py delete_database
  ```
