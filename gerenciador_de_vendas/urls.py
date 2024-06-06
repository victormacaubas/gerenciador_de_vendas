"""
URL configuration for gerenciador_de_vendas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vendas_app.views import (
    adjust_salaries_view,
    sorteio_view,
    estatisticas_view,
    home_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estatisticas/', estatisticas_view, name='estatisticas'),
    path('total-revenue-by-vendor/', total_revenue_by_vendor_view, name='total_revenue_by_vendor'),
    path('monthly-sales-by-product/', monthly_sales_by_product_view, name='monthly_sales_by_product'),
    path('top-clients/', top_clients_view, name='top_clients'),
    path('', home_view, name='home'),
]
