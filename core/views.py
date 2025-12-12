from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from .forms import RegistroForm

# 1. HOME - Lista produtos
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'core/home.html', {'produtos': produtos})

# 2. LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'core/login.html')

# 3. REGISTRO
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado! Faça login.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

# 4. LOGOUT
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado.')
    return redirect('home')

# 5. CARRINHO
@login_required
def carrinho_view(request):
    perfil = Perfil.objects.get(usuario=request.user)
    itens = Carrinho.objects.filter(cliente=perfil)
    total = sum(item.total_item() for item in itens)
    return render(request, 'core/carrinho.html', {'itens': itens, 'total': total})

# 6. ADICIONAR AO CARRINHO
@login_required
def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    perfil = Perfil.objects.get(usuario=request.user)
    
    if perfil.tipo != 'cliente':
        messages.error(request, 'Apenas clientes podem comprar.')
        return redirect('home')
    
    # Adiciona ou atualiza quantidade
    item, created = Carrinho.objects.get_or_create(
        cliente=perfil,
        produto=produto,
        defaults={'quantidade': 1}
    )
    
    if not created:
        item.quantidade += 1
        item.save()
    
    messages.success(request, f'{produto.nome} adicionado ao carrinho!')
    return redirect('home')

# 7. FINALIZAR PEDIDO
@login_required
def finalizar_pedido(request):
    perfil = Perfil.objects.get(usuario=request.user)
    itens_carrinho = Carrinho.objects.filter(cliente=perfil)
    
    if itens_carrinho.exists():
        # Cria pedido
        pedido = Pedido.objects.create(cliente=perfil, total=0)
        total_pedido = 0
        
        # Adiciona itens ao pedido
        for item in itens_carrinho:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco
            )
            total_pedido += item.total_item()
        
        # Atualiza total e limpa carrinho
        pedido.total = total_pedido
        pedido.save()
        itens_carrinho.delete()
        
        messages.success(request, 'Pedido realizado com sucesso!')
        return redirect('pedidos')
    
    messages.warning(request, 'Seu carrinho está vazio.')
    return redirect('carrinho')

# 8. PEDIDOS DO CLIENTE
@login_required
def pedidos_view(request):
    perfil = Perfil.objects.get(usuario=request.user)
    pedidos = Pedido.objects.filter(cliente=perfil).order_by('-criado_em')
    return render(request, 'core/pedidos.html', {'pedidos': pedidos})

# 9. DASHBOARD DO FEIRANTE
@login_required
def dashboard_view(request):
    perfil = Perfil.objects.get(usuario=request.user)
    
    if perfil.tipo != 'feirante':
        return redirect('home')
    
    try:
        banca = Banca.objects.get(feirante=perfil)
        produtos = Produto.objects.filter(banca=banca)
        
        # Estatísticas simples
        total_vendas = sum(p.pedido_set.count() * p.preco for p in produtos)
        
        return render(request, 'core/dashboard.html', {
            'banca': banca,
            'produtos': produtos,
            'total_vendas': total_vendas,
        })
    except Banca.DoesNotExist:
        messages.info(request, 'Você precisa criar uma banca primeiro.')
        return redirect('/admin/core/banca/add/')