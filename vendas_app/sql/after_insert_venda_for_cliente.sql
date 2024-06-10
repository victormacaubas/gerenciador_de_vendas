CREATE TRIGGER after_insert_venda_for_cliente
AFTER INSERT ON vendas_app_venda
FOR EACH ROW
BEGIN
    DECLARE total_spent DECIMAL(10, 2);
    DECLARE cashback DECIMAL(10, 2);
    DECLARE message_text VARCHAR(255);

    SELECT SUM(valor) INTO total_spent
    FROM vendas_app_venda
    WHERE cliente_id = NEW.cliente_id;

    IF total_spent > 500.00 THEN
        SET cashback = total_spent * 0.02;
        INSERT INTO vendas_app_clienteespecial (nome, idade, sexo, cliente_id, cashback)
        VALUES (
            (SELECT nome FROM vendas_app_cliente WHERE id = NEW.cliente_id),
            (SELECT idade FROM vendas_app_cliente WHERE id = NEW.cliente_id),
            (SELECT sexo FROM vendas_app_cliente WHERE id = NEW.cliente_id),
            NEW.cliente_id,
            cashback
        )
        ON DUPLICATE KEY UPDATE cashback = cashback + VALUES(cashback);

        SET message_text = CONCAT('Total cashback required: R$ ', FORMAT(cashback, 2));

        INSERT INTO vendas_app_eventlog_message (message, created_at)
        VALUES(message_text, NOW());
    END IF;
END;