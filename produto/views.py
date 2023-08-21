from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from pprint import pprint


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 3

class DatalheProdutos(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class DatalhesProdutos(View):
    pass

class AddAoCarrinho(View):
    def get(self, *args, **kwargs):

        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()

        #http_referer está guadandoa aba anterior
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        #variacao_id está guardando o "vid" da url, que vai funcionar como um id 
        variacao_id = self.request.GET.get('vid')

        #caso não tenha um vid(ele esteja vasio ou não exista), retorna a aba anterior e mostra uma mensagem
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)
        
        #recebe a variação apartir da variacao_id(o vid que ta sendo passado)
        #caso variacao_id não exista retorna erro 404
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        #criando as variaveis que vão ser passadas pra o carrinho
        produto = variacao.produto
        produto_nome = produto.nome
        produto_id = produto.id
        variacao_nome = variacao.nome or ''
        variacao_estoque = variacao.estoque
        preco_unitario = variacao.preco
        preco_unitario_promo = variacao.preco_promo
        quantidade = 1 
        slug = produto.slug
        imagem = produto.imagem

        #caso não tenha imagem passa espaço vazio
        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        #varifica se há produtop em estoque 
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        #se não tem um carrinho, então vai criar um carrinho 
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        #salva o carrinho nessa variavel carrinho
        carrinho = self.request.session['carrinho']

        #caso o id da varição esteja dentro do carrinho
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            #verifica se no estoque tem a quantidade que deve ser add ao carrinho
            #caso não tenha mostra mensagem de aviso e adiciona a quantidade que for possivel
            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x do produto: "{produto_nome}"'
                    f'Adcionamos {variacao_estoque}'
                )
                quantidade_carrinho = variacao_estoque

            #passa para o carrinho a quantide e o preço total(preço * quantidade)
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promo'] = preco_unitario_promo * quantidade_carrinho

        else:
            #passando os dados do produto pra dentro do carrinho
            carrinho[variacao_id] = {
                'produto_nome': produto_nome,
                'produto_id': produto_id, 
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promo': preco_unitario_promo,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promo': preco_unitario_promo,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        #salva
        self.request.session.save()

        #Mensagem de confirmação de adição ao carrinho
        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho'
        )

        print(carrinho)
        #retorna a aba antirior, no caso para o detelhs do produto
        return redirect(http_referer)

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):

        #http_referer está guadandoa aba anterior
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        #variacao_id está guardando o "vid" da url, que vai funcionar como um id 
        variacao_id = self.request.GET.get('vid')

        #se a variação não existe retorna para a pagina anterior 
        if not variacao_id:
            return redirect(http_referer)
        
        #se o carrinho não existe retorna para a pagina anterior 
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)
        
        #se o id da varição não exite no carrihno retorna para a pagina anterior
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)
        
        #guarda o carrinho em uma variavel carrinho
        carrinho = self.request.session['carrinho'][variacao_id]

        #mensssagem de sucesso 
        messages.success(
            self.request, 
            f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} foi removido do carrinho'
        )

        #deleta e salva 
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()

        return redirect(http_referer)

class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(self.request, 'produto/carrinho.html', contexto)

class Finalizar(View):
    pass