CREATE TRIGGER after_insert_venda
AFTER INSERT ON vendas_app_venda
FOR EACH ROW
BEGIN
    DECLARE total_sales DECIMAL(10, 2);
    DECLARE bonus DECIMAL(10, 2);
    DECLARE msg_txt VARCHAR(255);

    SELECT SUM(valor) INTO total_sales
    FROM vendas_app_venda
    WHERE vendedor_id = NEW.vendedor_id;

    IF total_sales > 1000.00 THEN
        SET bonus = total_sales * 0.05;
        UPDATE vendas_app_funcionario
        SET is_special = TRUE,
            salario = salario + bonus
        WHERE id = NEW.vendedor_id;

        SET msg_txt = CONCAT('Total bonus required: R$ ', FORMAT(bonus, 2));

        INSERT INTO eventlog_messages (message, created_at)
        VALUES (msg_txt, NOW());
    END IF;

    UPDATE vendas_app_produto
    SET quantidade = quantidade - NEW.quantidade
    WHERE id = NEW.produto_id;
END;
