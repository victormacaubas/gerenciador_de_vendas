from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Setup triggers for vendas_app_venda and vendas_app_cliente tables'

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
                    for statement in sql.split(';'):
                        if statement.strip():
                            cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS('Triggers created successfully!'))