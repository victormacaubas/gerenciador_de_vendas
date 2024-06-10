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

### Pré-requisitos

- Python 3.x
- Django
- MySQL
- python-decouple

### Passos para Configuração

1. **Clonar o Repositório**

```bash
git clone https://github.com/victormacaubas/gerenciador_de_vendas.git
cd gerenciador_de_vendas
```

2. **Criar e Ativar um Ambiente Virtual**

```bash
python -m venv venv
source venv/bin/activate # No Windows use: venv\Scripts\activate
```

3. **Instalar as Dependências**

```bash
pip install -r requirements.txt
```

4. **Configurar as Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
GERENTE_PASSWORD=your_gerente_password
FUNCIONARIO_PASSWORD=your_funcionario_password
SUPERUSER_PASSWORD=your_superuser_password
```

5. **Migrar o Banco de Dados**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Criar Usuários, Grupos, Triggers e Procedures**

```bash
python manage.py setup_triggers
python manage.py setup_procedures
python manage.py create_users_and_groups
```

7. **Executar o Servidor de Desenvolvimento**

```bash
python manage.py runserver
```

```

### Explicação:

1. **Introdução do App**: O contexto é descrito no início para dar uma visão geral do sistema.
2. **Tecnologias Utilizadas**: Explicação sobre Django e suas vantagens.
3. **Funcionalidades do Sistema**: Descrição das principais funcionalidades oferecidas pelo sistema.
4. **Como Executar o Projeto**: Instruções detalhadas para configuração e execução do projeto.
5. **Como Contribuir**: Instruções para quem deseja contribuir com o projeto.
6. **Licença**: Informação sobre a licença do projeto.
