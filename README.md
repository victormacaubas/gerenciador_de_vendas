# Sistema de E-commerce Paladins

<img src="/vendas_app/static/vendas_app/img/logo.png" alt="Logo" width="200"/>


 ## Grupo: 
 
 ### Danilo Souza , Igor Cassimiro ,  Victor Macaubas 

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

   Essas variáveis serão utilizadas pelo Docker para criar o banco de Dados MySQL do projeto.

   Crie um arquivo `.env` no root do projeto com as seguintes variáveis de ambiente:

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

   Os usuários criados pelo sistema para acessar o dashboard após a primeira migração serão: admin, gerente e funcionario. Para acessar como admin utilize a senha do super usuário.

4. **Construa e execute os contêiners**

   No root do projeto, execute o seguinte comando para construir e iniciar os contêineres Docker:

   ```sh
   docker-compose up --build
   ```

5. **Rode as migrações**

   Após os contêineres serem iniciados, abra outro terminal e execute o seguinte comando para rodar as migrações do banco de dados:

   ```sh
   docker-compose exec web python manage.py makemigrations vendas_app
   docker-compose exec web python manage.py migrate
   ```
   No Windows:

   ```sh
   cd gerenciador_de_vendas
   docker-compose exec web sh
   python manage.py makemigrations vendas_app
   python manage.py migrate
   ```

6. **Acesse a aplicação**

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

  No Windows:

  ```sh
   docker-compose exec web sh
   python manage.py delete_database
  ```

## Contexto
Este é um sistema de e-commerce para a venda de produtos diversos. O sistema foi desenvolvido com base nos seguintes requisitos:

- O sistema deve permitir a criação e a destruição completa do banco de dados;
- O sistema deve possuir 20 produtos, 5 cargos e 100 clientes nativos;
- O sistema deve possuir a opção de cadastrar apenas produtos e clientes.

## Tecnologias Utilizadas

### Django
Django é um framework de desenvolvimento web de alto nível, escrito em Python, que incentiva o desenvolvimento rápido e o design limpo e pragmático.

## Funcionalidades do Sistema

1. **Gerenciamento de Produtos**:
    - Cadastro, visualização e gerenciamento de produtos.
    - Controle de estoque com decremento automático após cada venda.

2. **Gerenciamento de Clientes**:
    - Cadastro, visualização e gerenciamento de clientes.
    - Suporte para clientes especiais com cashback.

3. **Gerenciamento de Vendas**:
    - Registro de vendas com atualização automática do estoque.
    - Relatórios de vendas por vendedor e por produto.

4. **Administração**:
    - Painel de administração customizado usando Django Jazzmin.
    - Controle de acesso baseado em grupos de usuários (funcionário, gerente e admin).

5. **Triggers e Procedures**:
    - Triggers para atualização automática do estoque e gestão de cashback.
    - Procedures para reajuste salarial, sorteio de clientes e estatísticas de vendas.

## Triggers

- **after_insert_venda**: Atualiza o estoque do produto após uma venda e calcula bônus para o vendedor.
- **after_insert_venda_for_cliente**: Adiciona ou atualiza o cashback para clientes especiais após uma venda.
- **after_update_cliente_especial**: Remove clientes especiais cujo cashback é zerado.

## Procedures

- **Reajuste(pct_reajuste, categoria)**: Aplica um reajuste salarial para todos os funcionários de uma categoria específica.
- **Sorteio()**: Realiza um sorteio para premiar um cliente com um voucher.
- **RegistrarVenda(produto_id)**: Reduz a quantidade de um produto na base de dados após uma venda.
- **Estatisticas()**: Gera estatísticas de vendas, incluindo produtos mais e menos vendidos, e meses de maior e menor venda.
