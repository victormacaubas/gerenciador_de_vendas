from django.contrib import admin
from django.http import HttpRequest
from .models import Cliente,Produto, Venda

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
    list_display = ('id_produto', 'id_vendedor', 'id_cliente', 'quantidade')
    search_fields = ('vendedor__nome', 'cliente__nome')

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Venda, VendaAdmin)

