from django.urls import path
from . import views

urlpatterns = [
    # Rotas principais
    path('', views.dashboard, name='dashboard'),
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/novo/', views.item_create, name='item_create'),
    path('inventario/<int:pk>/editar/', views.item_update, name='item_update'),
    path('inventario/<int:pk>/excluir/', views.item_delete, name='item_delete'),

    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/novo/', views.fornecedor_create, name='novo_fornecedor'),
    path('fornecedores/<int:pk>/editar/', views.fornecedor_update, name='fornecedor_update'),
    path('fornecedores/<int:pk>/excluir/', views.fornecedor_delete, name='fornecedor_delete'),

    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/novo/', views.pedido_create, name='novo_pedido'),
    path('pedidos/<int:pk>/editar/', views.pedido_update, name='pedido_update'),
    path('pedidos/<int:pk>/excluir/', views.pedido_delete, name='pedido_delete'),

    path('produto/novo/', views.novo_produto, name='novo_produto'),
    
    # Autenticação
    path('login/', views.EstoqueLoginView.as_view(), name='login'),
    path('logout/', views.EstoqueLogoutView.as_view(), name='logout'),
    
    # URLs antigas (redirecionamentos para compatibilidade)
    path('itens/', views.item_list, name='item_list'),
    path('itens/novo/', views.item_create, name='item_create_legacy'),
    path('fornecedores/criar/', views.fornecedor_create, name='fornecedor_create'),
]