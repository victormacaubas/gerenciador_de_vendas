from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Produto, Venda, Cliente
from django.db import connection
from .forms import VendaForm
from django.db import DatabaseError, transaction

def apply_salary_adjustment(percentage, category):
    with connection.cursor() as cursor:
        cursor.callproc('Reajuste', [percentage, category])

def execute_sorteio():
    with connection.cursor() as cursor:
        cursor.callproc('Sorteio')

def get_estatisticas():
    with connection.cursor() as cursor:
        cursor.callproc('Estatisticas')
        results = cursor.fetchall()
    return results

def adjust_salaries_view(request):
    if request.method == 'POST':
        percentage = request.POST.get('percentage')
        category = request.POST.get('category')
        
        try:
            percentage = float(percentage)
            apply_salary_adjustment(percentage, category)
            return JsonResponse({'status': 'success', 'message': 'Salaries adjusted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'vendas_app/adjust_salaries.html')

def sorteio_view(request):
    if request.method == 'POST':
        try:
            execute_sorteio()
            return JsonResponse({'status': 'success', 'message': 'Sorteio executed successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'vendas_app/sorteio.html')

def estatisticas_view(request):
    stats = get_estatisticas()
    context = {
        'stats': stats,
    }
    return render(request, 'vendas_app/estatisticas.html', context)

def home_view(request):
    return render(request, 'vendas_app/home.html')