from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FornecedorForm, ItemForm, PedidoForm, LojaForm, UsuarioCreationForm
from .models import Fornecedor, Item, Pedido, Loja

# --- Esta é a sua página principal ---
@login_required
def dashboard(request):
    total_itens = Item.objects.count()
    itens_baixo_estoque = Item.objects.filter(quantidade__lte=5).count()
    total_fornecedores = Fornecedor.objects.count()
    pedidos_pendentes = Pedido.objects.filter(status='PENDENTE').count()
    valor_total = Item.objects.aggregate(total=Sum('valor'))['total'] or 0

    overview_cards = [
        {'label': 'Vendas', 'value': 'R$ 832', 'meta': 'Últimos 7 dias', 'trend': '+8,3%', 'trend_type': 'up'},
        {'label': 'Receita', 'value': 'R$ 18.300', 'meta': 'Mês atual', 'trend': '+12%', 'trend_type': 'up'},
        {'label': 'Produtos', 'value': total_itens, 'meta': 'Cadastrados', 'trend': '+2 novos', 'trend_type': 'up'},
        {'label': 'Lucro', 'value': 'R$ 17.432', 'meta': 'Estimado', 'trend': '-3%', 'trend_type': 'down'},
    ]

    compras_cards = [
        {'label': 'Compras', 'value': 82, 'meta': 'na semana', 'trend': '+5%', 'trend_type': 'up'},
        {'label': 'Custo', 'value': 'R$ 13.573', 'meta': 'em pedidos', 'trend': '-2%', 'trend_type': 'down'},
        {'label': 'Cancelamentos', 'value': 5, 'meta': 'nos últimos 30 dias', 'trend': '-1%', 'trend_type': 'down'},
        {'label': 'Retorno', 'value': 'R$ 17.432', 'meta': 'estimado', 'trend': '+4%', 'trend_type': 'up'},
    ]

    resumo_inventario = [
        {'label': 'Quantidade em mãos', 'value': total_itens},
        {'label': 'A receber', 'value': pedidos_pendentes},
    ]

    resumo_produto = [
        {'label': 'Número de Fornecedores', 'value': total_fornecedores},
        {'label': 'Itens em baixa', 'value': itens_baixo_estoque},
    ]

    estoque_baixo = Item.objects.filter(quantidade__lte=10).order_by('quantidade')[:4]

    acoes_vendidas = [
        {'nome': 'Surf Excel', 'vendida': 30, 'restante': 12, 'preco': 'R$ 100'},
        {'nome': 'Rin', 'vendida': 21, 'restante': 15, 'preco': 'R$ 207'},
        {'nome': 'Parle G', 'vendida': 19, 'restante': 17, 'preco': 'R$ 105'},
    ]

    chart_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    chart_vendas = [50, 46, 49, 44, 48, 45]
    chart_compras = [38, 40, 35, 39, 36, 34]
    chart_points = [
        {'label': label, 'venda': venda, 'compra': compra}
        for label, venda, compra in zip(chart_labels, chart_vendas, chart_compras)
    ]

    contexto = {
        'overview_cards': overview_cards,
        'compras_cards': compras_cards,
        'resumo_inventario': resumo_inventario,
        'resumo_produto': resumo_produto,
        'chart_points': chart_points,
        'acoes_vendidas': acoes_vendidas,
        'estoque_baixo': estoque_baixo,
        'valor_total': valor_total,
    }
    return render(request, 'core/dashboard.html', contexto)

# --- Esta é a sua TELA DE LOGIN ---
class EstoqueLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sessão encerrada. Até logo!')
    return redirect('login')


def registrar(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = UsuarioCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuário criado com sucesso. Faça login para continuar.')
        return redirect('login')

    return render(request, 'core/registro.html', {'form': form})

@login_required
def inventario(request):
    itens = Item.objects.all().order_by('nome')
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if query:
        itens = itens.filter(nome__icontains=query)
    if status_filter:
        itens = itens.filter(status=status_filter)

    total_valor = Item.objects.aggregate(total=Sum('valor'))['total'] or 0

    contexto = {
        'itens': itens,
        'query': query or '',
        'status_filter': status_filter or '',
        'total_valor': total_valor,
    }
    return render(request, 'core/inventario.html', contexto)


@login_required
def item_create(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Item adicionado ao inventário.')
        return redirect('inventario')

    return render(request, 'core/item_form.html', {'form': form, 'titulo': 'Adicionar Item'})


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Item atualizado com sucesso.')
        return redirect('inventario')

    return render(request, 'core/item_form.html', {'form': form, 'titulo': 'Editar Item'})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item removido do inventário.')
        return redirect('inventario')

    contexto = {
        'object': item,
        'cancel_url': 'inventario',
        'titulo': 'Remover Item'
    }
    return render(request, 'core/confirm_delete.html', contexto)


@login_required
def fornecedores(request):
    fornecedores_queryset = Fornecedor.objects.all().order_by('nome')
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if query:
        fornecedores_queryset = fornecedores_queryset.filter(nome__icontains=query)
    if status_filter:
        fornecedores_queryset = fornecedores_queryset.filter(status=status_filter)

    contexto = {
        'fornecedores': fornecedores_queryset,
        'query': query or '',
        'status_filter': status_filter or '',
    }
    return render(request, 'core/fornecedores.html', contexto)


@login_required
def fornecedor_create(request):
    form = FornecedorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Fornecedor cadastrado com sucesso.')
        return redirect('fornecedores')

    return render(request, 'core/fornecedor_form.html', {'form': form, 'titulo': 'Novo Fornecedor'})


@login_required
def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    form = FornecedorForm(request.POST or None, instance=fornecedor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Fornecedor atualizado.')
        return redirect('fornecedores')

    return render(request, 'core/fornecedor_form.html', {'form': form, 'titulo': 'Editar Fornecedor'})


@login_required
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        messages.success(request, 'Fornecedor removido.')
        return redirect('fornecedores')

    contexto = {
        'object': fornecedor,
        'cancel_url': 'fornecedores',
        'titulo': 'Remover Fornecedor'
    }
    return render(request, 'core/confirm_delete.html', contexto)


@login_required
def pedidos(request):
    pedidos_queryset = Pedido.objects.select_related('fornecedor', 'item').order_by('-criado_em')
    status_filter = request.GET.get('status')
    fornecedor_filter = request.GET.get('fornecedor')

    if status_filter:
        pedidos_queryset = pedidos_queryset.filter(status=status_filter)
    if fornecedor_filter:
        pedidos_queryset = pedidos_queryset.filter(fornecedor_id=fornecedor_filter)

    contexto = {
        'pedidos': pedidos_queryset,
        'fornecedores': Fornecedor.objects.all().order_by('nome'),
        'status_filter': status_filter or '',
        'fornecedor_filter': fornecedor_filter or '',
    }
    return render(request, 'core/pedidos.html', contexto)


@login_required
def pedido_create(request):
    form = PedidoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pedido criado com sucesso.')
        return redirect('pedidos')

    return render(request, 'core/pedido_form.html', {'form': form, 'titulo': 'Novo Pedido'})


@login_required
def pedido_update(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    form = PedidoForm(request.POST or None, instance=pedido)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pedido atualizado.')
        return redirect('pedidos')

    return render(request, 'core/pedido_form.html', {'form': form, 'titulo': 'Editar Pedido'})


@login_required
def pedido_delete(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido excluído.')
        return redirect('pedidos')

    contexto = {
        'object': pedido,
        'cancel_url': 'pedidos',
        'titulo': 'Remover Pedido'
    }
    return render(request, 'core/confirm_delete.html', contexto)


@login_required
def gerenciar_loja(request):
    lojas_qs = Loja.objects.all()
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if query:
        lojas_qs = lojas_qs.filter(
            Q(nome__icontains=query) |
            Q(responsavel__icontains=query) |
            Q(cidade__icontains=query)
        )
    if status_filter:
        lojas_qs = lojas_qs.filter(status=status_filter)

    contexto = {
        'lojas': lojas_qs,
        'query': query or '',
        'status_filter': status_filter or '',
        'status_choices': Loja.STATUS_CHOICES,
        'total_lojas': lojas_qs.count(),
    }
    return render(request, 'core/lojas.html', contexto)


@login_required
def loja_create(request):
    form = LojaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Loja cadastrada com sucesso.')
        return redirect('gerenciar_loja')

    contexto = {'form': form, 'titulo': 'Nova Loja'}
    return render(request, 'core/loja_form.html', contexto)


@login_required
def loja_update(request, pk):
    loja = get_object_or_404(Loja, pk=pk)
    form = LojaForm(request.POST or None, instance=loja)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Loja atualizada com sucesso.')
        return redirect('gerenciar_loja')

    contexto = {'form': form, 'titulo': 'Editar Loja'}
    return render(request, 'core/loja_form.html', contexto)


@login_required
def loja_delete(request, pk):
    loja = get_object_or_404(Loja, pk=pk)
    if request.method == 'POST':
        loja.delete()
        messages.success(request, 'Loja removida.')
        return redirect('gerenciar_loja')

    contexto = {
        'object': loja,
        'cancel_url': 'gerenciar_loja',
        'titulo': 'Remover Loja'
    }
    return render(request, 'core/confirm_delete.html', contexto)


# URLs legadas
@login_required
def item_list(request):
    return inventario(request)


@login_required
def novo_fornecedor(request):
    return fornecedor_create(request)


@login_required
def novo_produto(request):
    return item_create(request)