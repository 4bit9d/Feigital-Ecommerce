from django.contrib import admin
from .models import *

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'telefone']

@admin.register(Banca)
class BancaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'feirante']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'banca', 'preco', 'estoque']
    list_filter = ['banca']

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'produto', 'quantidade', 'criado_em']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'status', 'total', 'criado_em']
    list_filter = ['status']

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'produto', 'quantidade', 'preco_unitario']