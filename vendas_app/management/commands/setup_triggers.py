from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'setup dos triggers para as tabelas vendas_app_venda e vendas_app_cliente'

    def handle(self, *args, **kwargs):
        trigger_sql = """
        CREATE TRIGGER after_insert_venda
        AFTER INSERT ON vendas_app_venda
        FOR EACH ROW
        BEGIN
            DECLARE total_sales DECIMAL(8, 2);
            DECLARE bonus DECIMAL(8, 2);
            DECLARE msg_txt VARCHAR(225);

            SELECT SUM(valor) INTO total_sales
            FROM vendas_app_venda
            WHERE id_vendedor_id = NEW.id_vendedor_id;

            IF total_sales > 1000.00 THEN
                SET bonus = total_sales * 0.05;
                UPDATE vendas_app_funcionario
                SET is_special = TRUE,
                    salario = salario + bonus
                WHERE id = NEW.id_vendedor_id;

                SET msg_txt = CONCAT('Bonus total necessário: R$ ', FORMAT(bonus,2));

                INSERT INTO eventlog_messages (message)
                VALUES(msg_txt);
            END IF;
        END;
        """

        trigger_cliente_sql = """
        CREATE TRIGGER after_insert_venda_for_cliente
        AFTER INSERT ON vendas_app_venda
        FOR EACH ROW
        BEGIN
            DECLARE total_spent DECIMAL(10, 2);
            DECLARE cashback DECIMAL(10, 2);
            DECLARE message_text VARCHAR(255);

            SELECT SUM(valor) INTO total_spent
            FROM vendas_app_venda
            WHERE id_cliente_id = NEW.id_cliente_id;

            IF total_spent > 500.00 THEN
                SET cashback = total_spent * 0.02;
                INSERT INTO vendas_app_clienteespecial (nome, idade, sexo, cliente_id, cashback)
                VALUES (
                    (SELECT nome FROM vendas_app_cliente WHERE id = NEW.id_cliente_id),
                    (SELECT idade FROM vendas_app_cliente WHERE id = NEW.id_cliente_id),
                    (SELECT sexo FROM vendas_app_cliente WHERE id = NEW.id_cliente_id),
                    NEW.id_cliente_id,
                    cashback
                )
                ON DUPLICATE KEY UPDATE cashback = cashback + VALUES(cashback);

                SET message_text = CONCAT('Total cashback required: R$ ', FORMAT(cashback, 2));

                INSERT INTO eventlog_messages (message)
                VALUES(message_text);
            END IF;
        END;
        """

        trigger_remove_cliente_especial_sql = """
        CREATE TRIGGER after_update_cliente_especial
        AFTER UPDATE ON vendas_app_clienteespecial
        FOR EACH ROW
        BEGIN
            IF NEW.cashback <= 0 THEN
                DELETE FROM vendas_app_clienteespecial WHERE id = NEW.id;
            END IF;
        END;
        """

        with connection.cursor() as cursor:
            cursor.execute("DROP TRIGGER IF EXISTS after_insert_venda")
            cursor.execute("DROP TRIGGER IF EXISTS after_insert_venda_for_cliente")
            cursor.execute("DROP TRIGGER IF EXISTS after_update_cliente_especial")
            cursor.execute(trigger_sql)
            cursor.execute(trigger_cliente_sql)
            cursor.execute(trigger_remove_cliente_especial_sql)

        self.stdout.write(self.style.SUCCESS('Triggers criados com sucesso!'))
