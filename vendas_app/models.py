from django.db import models

class cliente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    idade = models.IntegerField()
    nascimento = models.DateField()

class ClienteEspecial(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    idade = models.IntegerField()
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    cashback = models.DecimalField(max_digits=5, decimal_places=2)


# Create your models here.
