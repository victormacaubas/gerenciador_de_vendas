from django.contrib import admin
from django.urls import path
from django.http import HttpRequest
from .models import Cliente, Produto, Venda, Funcionario, Reajuste
from .views import total_revenue_by_vendor_view, monthly_sales_by_product_view, top_clients_view, estatisticas_view
 
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'valor', 'descricao')
    search_fields = ('nome',)
 
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)
 
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)
   
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'sexo', 'nascimento')
    search_fields = ('nome',)
 
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)
 
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)
 
 
class VendaAdmin(admin.ModelAdmin):
    list_display = ('produto', 'vendedor', 'cliente', 'quantidade','valor','data')
    search_fields = ('vendedor__nome', 'cliente__nome')
    exclude = ('valor',)
 
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)
 
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)

class ReadOnlyAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'sexo', 'cargo', 'salario', 'nascimento', 'is_special')
    search_fields = ('nome', 'cargo')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return self.model.objects.none()

class ReajusteForm(forms.ModelForm):
    class Meta:
        model = Reajuste
        fields = ['pct_reajuste', 'categoria']

    def save(self, commit=True):
        pct_reajuste = self.cleaned_data['pct_reajuste']
        categoria = self.cleaned_data['categoria']

        with connection.cursor() as cursor:
            cursor.callproc('Reajuste', [pct_reajuste, categoria])

        return super().save(commit=False)  # Do not save to the temporary model

class ReajusteAdmin(admin.ModelAdmin):
    form = ReajusteForm
    list_display = ['pct_reajuste', 'categoria']
    readonly_fields = ['pct_reajuste', 'categoria']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
 
class CustomAdminSite(admin.AdminSite):
    site_header = "Library Administration"
   
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('total-revenue-by-vendor/', total_revenue_by_vendor_view, name='total_revenue_by_vendor'),
            path('monthly-sales-by-product/', monthly_sales_by_product_view, name='monthly_sales_by_product'),
            path('top-clients/', top_clients_view, name='top_clients'),
            path('estatisticas/', estatisticas_view, name='estatisticas'),
        ]
        return my_urls + urls
   
admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(Funcionario, ReadOnlyAdmin)
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(Produto, ProdutoAdmin)
admin_site.register(Venda, VendaAdmin)
admin.site.register(Reajuste, ReajusteAdmin)