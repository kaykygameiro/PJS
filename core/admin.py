from django.contrib import admin
from .models import (
    Usuario, Fornecedor, Item, Funcionario,
    Atribuicao, OrdemCompra, HistoricoAuditoria, ItemOrdem, Pedido
)

# Isso faz as tabelas aparecerem no painel admin
admin.site.register(Usuario)
admin.site.register(Fornecedor)
admin.site.register(Item)
admin.site.register(Funcionario)
admin.site.register(Atribuicao)
admin.site.register(OrdemCompra)
admin.site.register(HistoricoAuditoria)
admin.site.register(ItemOrdem)
admin.site.register(Pedido)