from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Setup dos procedures do bando de dados'

    def handle(self, *args, **kwargs):
        proc_reajuste_sql = """
        CREATE PROCEDURE Reajuste(
            IN pct_reajuste DECIMAL(5, 2),
            IN categoria VARCHAR(100)
        )
        BEGIN
            UPDATE vendas_app_funcionario
            SET salario = salario * (1 + pct_reajuste / 100)
            WHERE cargo = categoria;
        END;
        """

        proc_sorteio_sql = """
        CREATE PROCEDURE Sorteio()
        BEGIN
            DECLARE cliente_id INT;
            DECLARE cliente_especial_id INT;
            DECLARE done INT DEFAULT 0;
            DECLARE cursor_clientes CURSOR FOR 
                SELECT id FROM vendas_app_cliente 
                ORDER BY RAND() LIMIT 1;
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

            OPEN cursor_clientes;

            sorteio_loop: LOOP
                FETCH cursor_clientes INTO cliente_id;
                IF done THEN
                    LEAVE sorteio_loop;
                END IF;

                -- Check if the selected client is in the ClienteEspecial table
                SELECT id INTO cliente_especial_id 
                FROM vendas_app_clienteespecial 
                WHERE cliente_id = cliente_id;

                -- If the client is special, award the voucher
                IF cliente_especial_id IS NOT NULL THEN
                    UPDATE vendas_app_clienteespecial 
                    SET cashback = cashback + 100.00 
                    WHERE cliente_id = cliente_id;

                    -- Prepare and emit a message
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = CONCAT('Voucher of R$ 100 awarded to client ID: ', cliente_id);
                END IF;

            END LOOP sorteio_loop;

            CLOSE cursor_clientes;
        END;
        """

        proc_registrar_venda_sql = """
        CREATE PROCEDURE RegistrarVenda(
            IN produto_id INT
        )
        BEGIN
            UPDATE vendas_app_produto
            SET quantidade = quantidade - 1
            WHERE id = produto_id;
        END;
        """

        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS Reajuste")
            cursor.execute(proc_reajuste_sql)
            cursor.execute("DROP PROCEDURE IF EXISTS Sorteio")
            cursor.execute(proc_sorteio_sql)
            cursor.execute("DROP PROCEDURE IF EXISTS RegistrarVenda")
            cursor.execute(proc_registrar_venda_sql)

        self.stdout.write(self.style.SUCCESS('Procedures criados corretamente.'))
