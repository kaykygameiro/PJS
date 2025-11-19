from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    PERFIS = [
        ('GERENTE_ESTOQUE', 'Gerente de Estoque'),
        ('TECNICO_TI', 'Técnico de TI'),
        ('GERENTE_COMPRAS', 'Gerente de Compras'),
    ]
    nome_completo = models.CharField(max_length=255, blank=True)
    perfil = models.CharField(max_length=50, choices=PERFIS, default='TECNICO_TI')

# Tabela FORNECEDOR
class Fornecedor(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('SUSPENSO', 'Suspenso'),
        ('ENCERRADO', 'Encerrado'),
    ]

    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    contato = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    produto_principal = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome

# Tabela ITEM
class Item(models.Model):
    STATUS_CHOICES = [('DISPONIVEL', 'Disponível'), ('INDISPONIVEL', 'Indisponível'), ('BAIXA_QUANTIDADE', 'Baixa Quantidade')]
    nome = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    localizacao = models.CharField(max_length=100, null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    data_aquisicao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DISPONIVEL')
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self): return self.nome

# Tabela FUNCIONARIO
class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    setor = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self): return self.nome

# Tabela ATRIBUICAO
class Atribuicao(models.Model):
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='ATIVO')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

# Tabela ORDEM_COMPRA
class OrdemCompra(models.Model):
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='PENDENTE')
    itens = models.ManyToManyField(Item, through='ItemOrdem')


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_TRANSITO', 'Em trânsito'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='pedidos')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='pedidos')
    quantidade = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    criado_em = models.DateTimeField(auto_now_add=True)
    entrega_prevista = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.item.nome}"

# Tabela ITEM_ORDEM
class ItemOrdem(models.Model):
    ordem_compra = models.ForeignKey(OrdemCompra, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

# Tabela HISTORICO_AUDITORIA
class HistoricoAuditoria(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)