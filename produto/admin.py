from django.contrib import admin
from . import models

class VariaçãoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1

class AvaliacaoInline(admin.TabularInline):
    model = models.AvaliacaoProduto
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_preco_formatado', 'get_preco_promo_formatado']

    inlines = [
        VariaçãoInline,
    ]

# Register your models here.
admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
admin.site.register(models.AvaliacaoProduto)