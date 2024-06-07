from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from vendas_app.models import Cliente, ClienteEspecial, Funcionario, Produto, Venda
from decouple import config

class Command(BaseCommand):
    help = 'Create default users and groups'

    def handle(self, *args, **kwargs):
        gerente_password = config('GERENTE_PASSWORD')
        funcionario_password = config('FUNCIONARIO_PASSWORD')
        superuser_password = config('SUPERUSER_PASSWORD')

        gerente_group, created = Group.objects.get_or_create(name='gerente')

        permissions = Permission.objects.filter(
            content_type__in=[
                ContentType.objects.get_for_model(Cliente),
                ContentType.objects.get_for_model(ClienteEspecial),
                ContentType.objects.get_for_model(Funcionario),
                ContentType.objects.get_for_model(Produto),
                ContentType.objects.get_for_model(Venda),
            ]
        )
        gerente_group.permissions.set(permissions)

        funcionario_group, created = Group.objects.get_or_create(name='funcionario')

        funcionario_group.permissions.set(
            Permission.objects.filter(
                codename__startswith='add'
            ) | Permission.objects.filter(
                codename__startswith='view'
            )
        )

        funcionario_group.permissions.remove(
            *Permission.objects.filter(codename__startswith='delete')
        )
        funcionario_group.permissions.remove(
            *Permission.objects.filter(codename__startswith='change')
        )

        print('Groups and permissions set up successfully.')

        gerente_user = User.objects.create_user(
            username='gerente',
            password=gerente_password,
            email='gerente@paladins.com'
        )
        gerente_user.groups.add(gerente_group)

        funcionario_user = User.objects.create_user(
            username='funcionario',
            password=funcionario_password,
            email='funcionario@paladins.com'
        )
        funcionario_user.groups.add(funcionario_group)

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password=superuser_password,
                email='admin@paladins.com'
            )

        gerente_user = User.objects.get(username='gerente')
        gerente_user.is_staff = True
        gerente_user.save()

        funcionario_user = User.objects.get(username='funcionario')
        funcionario_user.is_staff = True
        funcionario_user.save()

        self.stdout.write(self.style.SUCCESS('Successfully created users and groups'))

        call_command('setup_triggers')
        call_command('setup_procedures')

        self.stdout.write(self.style.SUCCESS('Successfully set up triggers and procedures'))
