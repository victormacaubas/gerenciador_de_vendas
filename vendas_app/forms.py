from django import forms
from .models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['id_produto', 'id_vendedor', 'id_cliente', 'quantidade']
