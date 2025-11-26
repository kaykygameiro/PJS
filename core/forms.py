from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Fornecedor, Item, Pedido, Loja, Usuario


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'contato', 'email', 'produto_principal', 'status', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do fornecedor'}),
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00'}),
            'contato': forms.TextInput(attrs={'placeholder': '(11) 99999-9999'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@fornecedor.com'}),
            'produto_principal': forms.TextInput(attrs={'placeholder': 'Produto fornecido'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'categoria', 'quantidade', 'status', 'valor']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Mouse Razer Viper 8'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ex: Periféricos'}),
            'quantidade': forms.NumberInput(attrs={'placeholder': 'Ex: 10'}),
            'valor': forms.NumberInput(attrs={'placeholder': 'Ex: 480.00'}),
        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['fornecedor', 'item', 'quantidade', 'status', 'entrega_prevista', 'observacoes']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'min': 1}),
            'entrega_prevista': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome', 'responsavel', 'telefone', 'email', 'endereco', 'cidade', 'estado', 'cep', 'inaugurada_em', 'status', 'observacoes']
        widgets = {
            'telefone': forms.TextInput(attrs={'placeholder': '(11) 99999-9999'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contato@loja.com'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Rua Exemplo, 123'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'São Paulo'}),
            'estado': forms.TextInput(attrs={'placeholder': 'SP'}),
            'cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'inaugurada_em': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome_completo', 'perfil']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@empresa.com'}),
            'nome_completo': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'perfil': forms.Select(),
        }