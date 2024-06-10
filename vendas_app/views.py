from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Produto, Venda, Cliente
from django.db import connection
from .forms import VendaForm
from django.db import DatabaseError, transaction

def get_estatisticas():
    with connection.cursor() as cursor:
        cursor.callproc('Estatisticas')
        results = cursor.fetchall()
    return results

def estatisticas_view(request):
    stats = get_estatisticas()
    context = {
        'stats': stats,
    }
    return render(request, 'vendas_app/estatisticas.html', context)

def total_revenue_by_vendor_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT f.nome AS vendedor, SUM(v.valor) AS total_revenue
            FROM vendas_app_venda v
            JOIN vendas_app_funcionario f ON v.vendedor_id = f.id
            GROUP BY f.nome
            ORDER BY total_revenue DESC;
        """)
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'vendas_app/total_revenue_by_vendor.html', context)

def monthly_sales_by_product_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.nome AS produto, DATE_FORMAT(v.data, '%Y-%m') AS mes, SUM(v.valor) AS total_sales
            FROM vendas_app_venda v
            JOIN vendas_app_produto p ON v.produto_id = p.id
            GROUP BY p.nome, mes
            ORDER BY p.nome, mes;
        """)
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'vendas_app/monthly_sales_by_product.html', context)

def top_clients_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.nome AS cliente, SUM(v.valor) AS total_purchases
            FROM vendas_app_venda v
            JOIN vendas_app_cliente c ON v.cliente_id = c.id
            GROUP BY c.nome
            ORDER BY total_purchases DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'vendas_app/top_clients.html', context)

