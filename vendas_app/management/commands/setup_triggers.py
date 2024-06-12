from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Criação dos triggers da database'

    def handle(self, *args, **kwargs):
        sql_files = [
            'vendas_app/sql/after_insert_venda.sql',
            'vendas_app/sql/after_insert_venda_for_cliente.sql',
            'vendas_app/sql/after_update_cliente_especial.sql'
        ]

        with connection.cursor() as cursor:
            cursor.execute("DROP TRIGGER IF EXISTS after_insert_venda")
            cursor.execute("DROP TRIGGER IF EXISTS after_insert_venda_for_cliente")
            cursor.execute("DROP TRIGGER IF EXISTS after_update_cliente_especial")
            
            for sql_file in sql_files:
                with open(sql_file, 'r') as file:
                    sql = file.read()
                    statements = sql.split('END;')
                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement + 'END;')

        self.stdout.write(self.style.SUCCESS('Triggers ativados com sucesso!'))