from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.views import View
import copy


from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/cirar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None

        #ususario logado
        if self.request.user.is_authenticated:
            self.perfil = models.PerfilUsuario.objects.filter(usuario=self.request.user).first()

            self.contexto = {
                'userform': forms.Userform(
                    data=self.request.POST or None, 
                    usuario=self.request.user, 
                    instance=self.request.user
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None, 
                    instance=self.perfil
                ),    
            }

        #ususario não logado
        else:
            self.contexto = {
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None
                ),
                'userform': forms.Userform(
                    data=self.request.POST or None
                )
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        self.rendenizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwarargs):
        return self.rendenizar

class Criar(BasePerfil):
    def post(self, *args, **kwaargs):

        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )

            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        first_name = self.userform.claened_data.get('first_name')
        last_name = self.userform.claened_data.get('last_name')
        email = self.userform.cleaned_data.get('email')

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name

            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil =  models.PerfilUsuario(**self.perfilform.cleaned_data)
                perfil.save()

            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario 
                perfil.save()
                
        # Usário não logado
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(self.request, username=usuario, password=password)

            if autentica:
                login(self.request, user=usuario)


        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request, 'Seu cadastro foi criado ou atualizado'
        )

        messages.success(
            self.request, 'Você fez login e pode concluir sua compra'
        )

        return redirect('produto:carrinho')
        return self.rendenizar

class Atualizar(BasePerfil):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')

class Login(View):
    pass

class Logout(View):
    pass
