DELIMITER //
CREATE PROCEDURE Reajuste(
    IN pct_reajuste DECIMAL(5, 2),
    IN categoria VARCHAR(100)
)
BEGIN
    UPDATE vendas_app_funcionario
    SET salario = salario * (1 + pct_reajuste / 100)
    WHERE cargo = categoria;
END//

DELIMITER ;