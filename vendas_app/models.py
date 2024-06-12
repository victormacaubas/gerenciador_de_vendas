from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone

class Cliente(models.Model):

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1)
    idade = models.IntegerField()
    nascimento = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_gender',
                check=Q(sexo = 'm') | Q(sexo = 'f') | Q(sexo = 'o'),
                violation_error_message='Sexo inválido, escolha entre masculino, feminino ou outro.'
            )
        ]
    
    def __str__(self):
        return self.nome

class ClienteEspecial(models.Model):

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cashback = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_gender_cliente_especial',
                check=Q(sexo = 'm') | Q(sexo = 'f') | Q(sexo = 'o'),
                violation_error_message='Sexo inválido, escolha entre masculino, feminino ou outro.'
            )
        ]
    
    def __str__(self):
        return self.nome

class Funcionario(models.Model):

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1)
    cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=8, decimal_places=2)
    nascimento = models.DateField()
    is_special = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_role',
                check=Q(cargo = 'gerente') | Q(cargo = 'vendedor') | Q(cargo = 'CEO'),
                violation_error_message='Cargo inválido, escolha entre gerente, vendedor ou CEO.'
            ),
            models.CheckConstraint(
                name='check_gender_funcionario',
                check=Q(sexo = 'm') | Q(sexo = 'f') | Q(sexo = 'o'),
                violation_error_message='Sexo inválido, escolha entre masculino, feminino ou outro.'
            )
        ]
    
    def __str__(self):
        return self.nome

class Produto(models.Model):

    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_value',
                check=Q(valor__gte=0),
                violation_error_message='Valor do produto deve ser maior ou igual a zero.'
            )
        ]

    def __str__(self):
        return self.nome

class EventLog_Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

class Reajuste(models.Model):
    pct_reajuste = models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return f"Reajuste {self.pct_reajuste}% for {self.categoria}"

class Venda(models.Model):

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    hora= models.TimeField(auto_now_add=True)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # This will be auto-calculated

    def __str__(self):
        return f"Venda de {self.produto.nome} - {self.vendedor.nome} to {self.cliente.nome}"
        
@receiver(pre_save, sender=Venda)
def calculate_valor(sender, instance, **kwargs):
    instance.valor = instance.produto.valor * instance.quantidade