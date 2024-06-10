CREATE PROCEDURE RegistrarVenda(
    IN produto_id INT
)
BEGIN
    UPDATE vendas_app_produto
    SET quantidade = quantidade - 1
    WHERE id = produto_id;
END;