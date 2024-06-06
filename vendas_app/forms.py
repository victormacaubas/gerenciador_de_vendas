from django import forms
from .models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['vendedor', 'cliente', 'produto', 'quantidade']  # 'valor' is not included
