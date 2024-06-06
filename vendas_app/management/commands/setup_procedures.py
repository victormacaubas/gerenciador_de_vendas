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
            DECLARE msg_txt VARCHAR(255);

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

                SELECT id INTO cliente_especial_id 
                FROM vendas_app_clienteespecial 
                WHERE cliente_id = cliente_id;
                LIMIT 1;

                IF cliente_especial_id IS NOT NULL THEN
                    UPDATE vendas_app_clienteespecial 
                    SET cashback = cashback + 100.00 
                    WHERE cliente_id = cliente_id;

                    SET msg_txt = CONCAT('Voucher of R$ 100 awarded to client ID: ', cliente_id);

                INSERT INTO eventlog_messages (message)
                VALUES(msg_txt);
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

        proc_estatisticas_sql = """
        CREATE PROCEDURE Estatisticas()
        BEGIN
            DECLARE most_sold_product_id INT;
            DECLARE least_sold_product_id INT;
            DECLARE most_sold_product_name VARCHAR(100);
            DECLARE least_sold_product_name VARCHAR(100);
            DECLARE associated_vendedor_name VARCHAR(100);
            DECLARE revenue_most_sold_product DECIMAL(10, 2);
            DECLARE revenue_least_sold_product DECIMAL(10, 2);
            DECLARE highest_sales_month_most_sold_product VARCHAR(7);
            DECLARE lowest_sales_month_most_sold_product VARCHAR(7);
            DECLARE highest_sales_month_least_sold_product VARCHAR(7);
            DECLARE lowest_sales_month_least_sold_product VARCHAR(7);
            
            SELECT id_produto_id, SUM(valor) INTO most_sold_product_id, revenue_most_sold_product
            FROM vendas_app_venda
            GROUP BY id_produto_id
            ORDER BY SUM(valor) DESC
            LIMIT 1;

            SELECT id_produto_id, SUM(valor) INTO least_sold_product_id, revenue_least_sold_product
            FROM vendas_app_venda
            GROUP BY id_produto_id
            ORDER BY SUM(valor) ASC
            LIMIT 1;

            SELECT nome INTO most_sold_product_name FROM vendas_app_produto WHERE id = most_sold_product_id;
            SELECT nome INTO least_sold_product_name FROM vendas_app_produto WHERE id = least_sold_product_id;

            SELECT f.nome INTO associated_vendedor_name
            FROM vendas_app_venda v
            JOIN vendas_app_funcionario f ON v.id_vendedor_id = f.id
            WHERE v.id_produto_id = most_sold_product_id
            GROUP BY v.id_vendedor_id
            ORDER BY COUNT(*) DESC
            LIMIT 1;

            SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO highest_sales_month_most_sold_product, @max_sales
            FROM vendas_app_venda
            WHERE id_produto_id = most_sold_product_id
            GROUP BY DATE_FORMAT(data, '%Y-%m')
            ORDER BY SUM(valor) DESC
            LIMIT 1;

            SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO lowest_sales_month_most_sold_product, @min_sales
            FROM vendas_app_venda
            WHERE id_produto_id = most_sold_product_id
            GROUP BY DATE_FORMAT(data, '%Y-%m')
            ORDER BY SUM(valor) ASC
            LIMIT 1;

            SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO highest_sales_month_least_sold_product, @max_sales
            FROM vendas_app_venda
            WHERE id_produto_id = least_sold_product_id
            GROUP BY DATE_FORMAT(data, '%Y-%m')
            ORDER BY SUM(valor) DESC
            LIMIT 1;

            SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO lowest_sales_month_least_sold_product, @min_sales
            FROM vendas_app_venda
            WHERE id_produto_id = least_sold_product_id
            GROUP BY DATE_FORMAT(data, '%Y-%m')
            ORDER BY SUM(valor) ASC
            LIMIT 1;

            SELECT
                most_sold_product_name AS ProdutoMaisVendido,
                associated_vendedor_name AS VendedorAssociado,
                least_sold_product_name AS ProdutoMenosVendido,
                revenue_most_sold_product AS ValorGanhoProdutoMaisVendido,
                highest_sales_month_most_sold_product AS MesMaiorVendaProdutoMaisVendido,
                lowest_sales_month_most_sold_product AS MesMenorVendaProdutoMaisVendido,
                revenue_least_sold_product AS ValorGanhoProdutoMenosVendido,
                highest_sales_month_least_sold_product AS MesMaiorVendaProdutoMenosVendido,
                lowest_sales_month_least_sold_product AS MesMenorVendaProdutoMenosVendido;
        END;
        """

        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS Reajuste")
            cursor.execute(proc_reajuste_sql)
            cursor.execute("DROP PROCEDURE IF EXISTS Sorteio")
            cursor.execute(proc_sorteio_sql)
            cursor.execute("DROP PROCEDURE IF EXISTS RegistrarVenda")
            cursor.execute(proc_registrar_venda_sql)
            cursor.execute("DROP PROCEDURE IF EXISTS Estatisticas")
            cursor.execute(proc_estatisticas_sql)

        self.stdout.write(self.style.SUCCESS('Procedures criados corretamente.'))
