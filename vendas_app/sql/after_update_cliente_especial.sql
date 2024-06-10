DELIMITER //

CREATE TRIGGER after_update_cliente_especial
AFTER UPDATE ON vendas_app_clienteespecial
FOR EACH ROW
BEGIN
    IF NEW.cashback <= 0 THEN
        DELETE FROM vendas_app_clienteespecial WHERE id = NEW.id;
    END IF;
END//

DELIMITER ;