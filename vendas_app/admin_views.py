from django.urls import path
from .views import (
    monthly_sales_by_product_view,
    top_clients_view,
    estatisticas_view,
    total_revenue_by_vendor_view,
)

def get_admin_urls(urls):
    def get_urls():
        my_urls = [
            path('total-revenue-by-vendor/', total_revenue_by_vendor_view, name='total_revenue_by_vendor'),
            path('monthly-sales-by-product/', monthly_sales_by_product_view, name='monthly_sales_by_product'),
            path('top-clients/', top_clients_view, name='top_clients'),
            path('estatisticas/', estatisticas_view, name='estatisticas'),
        ]
        return my_urls + urls
    return get_urls

from django.contrib import admin
admin.site.get_urls = get_admin_urls(admin.site.get_urls)