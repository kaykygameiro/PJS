from django import forms
from .models import Fornecedor, Item, Pedido


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
        fields = ['nome', 'categoria', 'localizacao', 'quantidade', 'data_aquisicao', 'status', 'valor']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Mouse Razer Viper 8'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ex: Periféricos'}),
            'localizacao': forms.TextInput(attrs={'placeholder': 'Ex: Prateleira A-05'}),
            'quantidade': forms.NumberInput(attrs={'placeholder': 'Ex: 10'}),
            'data_aquisicao': forms.DateInput(attrs={'type': 'date'}),
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