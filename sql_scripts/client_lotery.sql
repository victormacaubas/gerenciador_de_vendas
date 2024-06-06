DELIMITER //
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

        IF cliente_especial_id IS NOT NULL THEN
            UPDATE vendas_app_clienteespecial 
            SET cashback = cashback + 100.00 
            WHERE cliente_id = cliente_id;

            SET msg_txt = CONCAT('Voucher of R$ 100 awarded to client ID: ', cliente_id);

            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = msg_txt
        END IF;

    END LOOP sorteio_loop;

    CLOSE cursor_clientes;
END//
DELIMITER ;