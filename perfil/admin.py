from django.contrib import admin
from . import models

class EnderecoInline(admin.TabularInline):
    model = models.EnderecoUsuario
    extra = 1

class PerfilAdmin(admin.ModelAdmin):
    inlines = [
        EnderecoInline
    ]

# Register your models here.
admin.site.register(models.PerfilUsuario, PerfilAdmin)
admin.site.register(models.EnderecoUsuario)