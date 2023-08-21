from django.urls import path
from . import views

app_name = 'pedido' #pedido:{name}

urlpatterns = [
    path('', views.Pagar.as_view(), name='pagar'),
    path('fecharpedido/', views.FecharPedido.as_view(), name='fecharpedido/'),
    path('detalhes/<int:pk>', views.Detalhes.as_view(), name='detalhes'),
]
