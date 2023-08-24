from django.db import models
import os 
from PIL import Image 
from django.db import models
from E_commerce import settings
from django.utils.text import slugify
from utils import utils
from django.contrib.auth.models import User 

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.CharField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promo = models.FloatField(default=0, verbose_name='Preço Promo')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promo_formatado(self):
        return utils.formata_preco(self.preco_marketing_promo)
    get_preco_promo_formatado.short_description = 'Preço Promo'

    #Redefine tamnho da imagem
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwergs):

        if not self.slug:
            slug= f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwergs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome
    

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True)
    preco = models.FloatField()
    preco_promo = models.FloatField(default=0)
    estoque = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

class AvaliacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    nota = models.FloatField()
    comentario =models.CharField( max_length=255)

    def __str__(self):
        return self. nome or self.produto.nome
        
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'