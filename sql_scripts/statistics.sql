DELIMITER //

CREATE PROCEDURE Estatisticas()
BEGIN
    DECLARE produto_mais_vendido INT;
    DECLARE produto_menos_vendido INT;
    DECLARE vendedor_mais_vendido INT;
    DECLARE valor_mais_vendido DECIMAL(10, 2);
    DECLARE valor_menos_vendido DECIMAL(10, 2);
    DECLARE mes_maior_venda_mais_vendido VARCHAR(7);
    DECLARE mes_menor_venda_mais_vendido VARCHAR(7);
    DECLARE mes_maior_venda_menos_vendido VARCHAR(7);
    DECLARE mes_menor_venda_menos_vendido VARCHAR(7);

    -- Produto mais vendido
    SELECT id_produto INTO produto_mais_vendido
    FROM (SELECT id_produto, COUNT(*) AS total_vendas
          FROM vendas_app_venda
          GROUP BY id_produto
          ORDER BY total_vendas DESC
          LIMIT 1) AS subquery;

    -- Vendedor associado ao produto mais vendido
    SELECT id_vendedor INTO vendedor_mais_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_mais_vendido
    GROUP BY id_vendedor
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Produto menos vendido
    SELECT id_produto INTO produto_menos_vendido
    FROM (SELECT id_produto, COUNT(*) AS total_vendas
          FROM vendas_app_venda
          GROUP BY id_produto
          ORDER BY total_vendas ASC
          LIMIT 1) AS subquery;

    -- Valor ganho com o produto mais vendido
    SELECT SUM(valor) INTO valor_mais_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_mais_vendido;

    -- Mês de maior vendas do produto mais vendido
    SELECT DATE_FORMAT(data, '%Y-%m') INTO mes_maior_venda_mais_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_mais_vendido
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Mês de menor vendas do produto mais vendido
    SELECT DATE_FORMAT(data, '%Y-%m') INTO mes_menor_venda_mais_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_mais_vendido
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY COUNT(*) ASC
    LIMIT 1;

    -- Valor ganho com o produto menos vendido
    SELECT SUM(valor) INTO valor_menos_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_menos_vendido;

    -- Mês de maior vendas do produto menos vendido
    SELECT DATE_FORMAT(data, '%Y-%m') INTO mes_maior_venda_menos_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_menos_vendido
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Mês de menor vendas do produto menos vendido
    SELECT DATE_FORMAT(data, '%Y-%m') INTO mes_menor_venda_menos_vendido
    FROM vendas_app_venda
    WHERE id_produto = produto_menos_vendido
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY COUNT(*) ASC
    LIMIT 1;

    -- Select results
    SELECT produto_mais_vendido AS ProdutoMaisVendido,
           vendedor_mais_vendido AS VendedorMaisVendido,
           produto_menos_vendido AS ProdutoMenosVendido,
           valor_mais_vendido AS ValorMaisVendido,
           mes_maior_venda_mais_vendido AS MesMaiorVendaMaisVendido,
           mes_menor_venda_mais_vendido AS MesMenorVendaMaisVendido,
           valor_menos_vendido AS ValorMenosVendido,
           mes_maior_venda_menos_vendido AS MesMaiorVendaMenosVendido,
           mes_menor_venda_menos_vendido AS MesMenorVendaMenosVendido;
END//

DELIMITER ;
