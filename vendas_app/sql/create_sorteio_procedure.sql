DELIMITER //

CREATE PROCEDURE Sorteio()
BEGIN
    DECLARE cliente_id INT;
    DECLARE cliente_especial_id INT;
    DECLARE done INT DEFAULT 0;
    DECLARE msg_txt VARCHAR(255);
    DECLARE voucher_amount DECIMAL(10, 2);

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
        WHERE cliente_id = cliente_id
        LIMIT 1;

        IF cliente_especial_id IS NOT NULL THEN
            SET voucher_amount = 200.00;
            UPDATE vendas_app_clienteespecial 
            SET cashback = cashback + voucher_amount 
            WHERE cliente_id = cliente_id;
            SET msg_txt = CONCAT('Voucher of R$ ', voucher_amount, ' awarded to special client ID: ', cliente_id);
        ELSE
            SET voucher_amount = 100.00;
            INSERT INTO vendas_app_clienteespecial (nome, idade, sexo, cliente_id, cashback)
            SELECT nome, idade, sexo, id, voucher_amount
            FROM vendas_app_cliente
            WHERE id = cliente_id;
            SET msg_txt = CONCAT('Voucher of R$ ', voucher_amount, ' awarded to regular client ID: ', cliente_id);
        END IF;

        INSERT INTO vendas_app_eventlog_message (message, created_at)
        VALUES(msg_txt, NOW());

    END LOOP sorteio_loop;

    CLOSE cursor_clientes;
END//

DELIMITER ;