CREATE PROCEDURE Estatisticas()
BEGIN
    DECLARE most_sold_product_id INT;
    DECLARE least_sold_product_id INT;
    DECLARE most_sold_product_name VARCHAR(100);
    DECLARE least_sold_product_name VARCHAR(100);
    DECLARE associated_vendedor_name VARCHAR(100);
    DECLARE revenue_most_sold_product DECIMAL(10, 2);
    DECLARE revenue_least_sold_product DECIMAL(10, 2);
    DECLARE highest_sales_month_most_sold_product VARCHAR(7);
    DECLARE lowest_sales_month_most_sold_product VARCHAR(7);
    DECLARE highest_sales_month_least_sold_product VARCHAR(7);
    DECLARE lowest_sales_month_least_sold_product VARCHAR(7);

    SELECT produto_id, SUM(valor) INTO most_sold_product_id, revenue_most_sold_product
    FROM vendas_app_venda
    GROUP BY produto_id
    ORDER BY SUM(valor) DESC
    LIMIT 1;

    SELECT produto_id, SUM(valor) INTO least_sold_product_id, revenue_least_sold_product
    FROM vendas_app_venda
    GROUP BY produto_id
    ORDER BY SUM(valor) ASC
    LIMIT 1;

    SELECT nome INTO most_sold_product_name FROM vendas_app_produto WHERE id = most_sold_product_id;
    SELECT nome INTO least_sold_product_name FROM vendas_app_produto WHERE id = least_sold_product_id;

    SELECT f.nome INTO associated_vendedor_name
    FROM vendas_app_venda v
    JOIN vendas_app_funcionario f ON v.vendedor_id = f.id
    WHERE v.produto_id = most_sold_product_id
    GROUP BY v.vendedor_id
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO highest_sales_month_most_sold_product, @max_sales
    FROM vendas_app_venda
    WHERE produto_id = most_sold_product_id
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY SUM(valor) DESC
    LIMIT 1;

    SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO lowest_sales_month_most_sold_product, @min_sales
    FROM vendas_app_venda
    WHERE produto_id = most_sold_product_id
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY SUM(valor) ASC
    LIMIT 1;

    SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO highest_sales_month_least_sold_product, @max_sales
    FROM vendas_app_venda
    WHERE produto_id = least_sold_product_id
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY SUM(valor) DESC
    LIMIT 1;

    SELECT DATE_FORMAT(data, '%Y-%m'), SUM(valor) INTO lowest_sales_month_least_sold_product, @min_sales
    FROM vendas_app_venda
    WHERE produto_id = least_sold_product_id
    GROUP BY DATE_FORMAT(data, '%Y-%m')
    ORDER BY SUM(valor) ASC
    LIMIT 1;

    SELECT
        most_sold_product_name AS ProdutoMaisVendido,
        associated_vendedor_name AS VendedorAssociado,
        least_sold_product_name AS ProdutoMenosVendido,
        revenue_most_sold_product AS ValorGanhoProdutoMaisVendido,
        highest_sales_month_most_sold_product AS MesMaiorVendaProdutoMaisVendido,
        lowest_sales_month_most_sold_product AS MesMenorVendaProdutoMaisVendido,
        revenue_least_sold_product AS ValorGanhoProdutoMenosVendido,
        highest_sales_month_least_sold_product AS MesMaiorVendaProdutoMenosVendido,
        lowest_sales_month_least_sold_product AS MesMenorVendaProdutoMenosVendido;
END;