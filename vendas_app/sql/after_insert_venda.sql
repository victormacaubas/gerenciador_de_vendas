CREATE TRIGGER after_insert_venda
AFTER INSERT ON vendas_app_venda
FOR EACH ROW
BEGIN
    DECLARE total_sales DECIMAL(8, 2);
    DECLARE bonus DECIMAL(8, 2);
    DECLARE msg_txt VARCHAR(225);

    SELECT SUM(valor) INTO total_sales
    FROM vendas_app_venda
    WHERE vendedor_id = NEW.vendedor_id;

    IF total_sales > 1000.00 THEN
        SET bonus = total_sales * 0.05;
        UPDATE vendas_app_funcionario
        SET is_special = TRUE,
            salario = salario + bonus
        WHERE id = NEW.vendedor_id;

        SET msg_txt = CONCAT('Bonus total necessário: R$ ', FORMAT(bonus,2));

        INSERT INTO vendas_app_eventlog_message (message, created_at)
        VALUES(msg_txt, NOW());
    END IF;
    CALL RegistrarVenda(NEW.produto_id);
END;