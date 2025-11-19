from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FornecedorForm, ItemForm, PedidoForm
from .models import Fornecedor, Item, Pedido

# --- Esta é a sua página principal ---
@login_required
def dashboard(request):
    total_itens = Item.objects.count()
    itens_baixo_estoque = Item.objects.filter(quantidade__lte=5).count()
    total_fornecedores = Fornecedor.objects.count()
    pedidos_pendentes = Pedido.objects.filter(status='PENDENTE').count()

    contexto = {
        'total_itens': total_itens,
        'itens_baixo_estoque': itens_baixo_estoque,
        'total_fornecedores': total_fornecedores,
        'pedidos_pendentes': pedidos_pendentes,
    }
    return render(request, 'core/dashboard.html', contexto)

# --- Esta é a sua TELA DE LOGIN ---
class EstoqueLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True 

# --- Esta é a lógica de LOGOUT ---
class EstoqueLogoutView(LogoutView):
    pass # Deixe assim, ele vai usar o settings.py

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