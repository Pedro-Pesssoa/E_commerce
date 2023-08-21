from django.contrib import admin
from . import models

class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]

# Register your models here.
admin.site.register(models.Pedidos, PedidoAdmin)
admin.site.register(models.ItemPedido)
