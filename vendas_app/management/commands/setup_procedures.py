from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Criação dos procedures da database'

    def handle(self, *args, **kwargs):
        sql_files = [
            'vendas_app/sql/create_reajuste_procedure.sql',
            'vendas_app/sql/create_sorteio_procedure.sql',
            'vendas_app/sql/create_registrar_venda_procedure.sql',
            'vendas_app/sql/create_estatisticas_procedure.sql'
        ]

        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS Reajuste")
            cursor.execute("DROP PROCEDURE IF EXISTS Sorteio")
            cursor.execute("DROP PROCEDURE IF EXISTS RegistrarVenda")
            cursor.execute("DROP PROCEDURE IF EXISTS Estatisticas")

            for sql_file in sql_files:
                with open(sql_file, 'r') as file:
                    sql = file.read()
                    statements = sql.split('END;')
                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement + 'END;')

        self.stdout.write(self.style.SUCCESS('Procedures criados com sucesso!'))