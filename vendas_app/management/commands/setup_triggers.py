from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Cria um trigger para adicionar um bonus ao salario do vendedor quando ele atingir um total de vendas maior que R$ 1000.00'

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

                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = msg_txt;
            END IF;
        END;
        """

        with connection.cursor() as cursor:
            cursor.execute("DROP TRIGGER IF EXISTS after_insert_venda")
            cursor.execute(trigger_sql)

        self.stdout.write(self.style.SUCCESS('Trigger criado com sucesso!'))
