from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import qrcode
from io import BytesIO
from django.core.files import File

# 1. Perfil de usuário (feirante ou cliente)
class Perfil(models.Model):
    TIPO_CHOICES = [
        ('feirante', 'Feirante'),
        ('cliente', 'Cliente'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    telefone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.usuario.username} ({self.tipo})"

# 2. Banca do feirante
class Banca(models.Model):
    feirante = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'feirante'})
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome

# 3. Produto da banca
class Produto(models.Model):
    banca = models.ForeignKey(Banca, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome} - R${self.preco}"

# 4. Carrinho do cliente
class Carrinho(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'cliente'})
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def total_item(self):
        return self.produto.preco * self.quantidade

# 5. Pedido final
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('preparando', 'Em Preparação'),
        ('pronto', 'Pronto para Retirada'),
        ('entregue', 'Entregue'),
    ]
    
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'cliente'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    
    def gerar_qrcode(self):
        qr = qrcode.make(f"Pedido #{self.id} - Cliente: {self.cliente.usuario.username}")
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        self.qr_code.save(f'qrcode_pedido_{self.id}.png', File(buffer), save=False)
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.gerar_qrcode()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

# 6. Itens do pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def total(self):
        return self.preco_unitario * self.quantidade