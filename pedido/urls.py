from django.urls import path
from . import views

app_name = 'pedido' #pedido:{name}

urlpatterns = [
    path('', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedodo/'),
    path('detalhes/<int:pk>', views.Detalhes.as_view(), name='detalhes'),
]
