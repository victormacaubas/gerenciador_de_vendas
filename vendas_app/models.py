from django.db import models
from django.db.models import Q

# Create your models here.
GENDER_CHOICES = [
        ("m", "M"),
        ("f", "F"),
        ("o", "O"),
    ]

ROLE_CHOICES = [
        ("gerente", "Gerente"), 
        ("vendedor", "Vendedor"), 
        ("ceo", "CEO")
    ]

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

class ClienteEspecial(models.Model):

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cashback = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_gender_cliente_especial',
                check=Q(sexo = 'm') | Q(sexo = 'f') | Q(sexo = 'o'),
                violation_error_message='Sexo inválido, escolha entre masculino, feminino ou outro.'
            )
        ]


class Funcionario(models.Model):

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1)
    cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=5, decimal_places=2)
    nascimento = models.DateField()
    is_special = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_role',
                check=Q(cargo = 'gerente') | Q(cargo = 'vendedor') | Q(cargo = 'ceo'),
                violation_error_message='Cargo inválido, escolha entre gerente, vendedor ou CEO.'
            ),
            models.CheckConstraint(
                name='check_gender_funcionario',
                check=Q(sexo = 'm') | Q(sexo = 'f') | Q(sexo = 'o'),
                violation_error_message='Sexo inválido, escolha entre masculino, feminino ou outro.'
            )
        ]

class Produto(models.Model):

    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_value',
                check=Q(valor__gte=0),
                violation_error_message='Valor do produto deve ser maior ou igual a zero.'
            )
        ]

class Venda(models.Model):

    id_vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField()

