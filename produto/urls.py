from django.urls import path
from . import views

app_name = 'produto' #produto:{name}

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DatalheProdutos.as_view(), name='detalhe'),
    path('addaocarrinho/', views.AddAoCarrinho.as_view(), name='addaocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),

]
