from django import forms
from .models import Venda, Reajuste

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['produto', 'vendedor', 'cliente', 'quantidade']

class ReajusteForm(forms.ModelForm):
    class Meta:
        model = Reajuste
        fields = ['pct_reajuste', 'categoria']