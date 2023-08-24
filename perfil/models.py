from django.db import models
from django.contrib.auth.models import User 
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf

# Create your models here.
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.usuario}'
    
    def clean(self):
        erro_messages ={}

        if not valida_cpf(self.cpf):
            erro_messages['cpf'] = 'Digite um cpf valido'

        if erro_messages:
            raise ValidationError(erro_messages)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

class EnderecoUsuario(models.Model):
    perfil_usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    rua = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        default='RN',
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.perfil_usuario}'

    def clean(self):
        erro_messages = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            erro_messages['cep'] = 'CEP inválido, digite os 8 digitos do cep'

        if erro_messages:
            raise ValidationError(erro_messages)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'