from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from .models import Fornecedor, Item, Pedido


class CrudViewsTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='tester', password='senha-super-secreta'
		)
		self.client.force_login(self.user)

	def test_can_create_fornecedor(self):
		response = self.client.post(reverse('novo_fornecedor'), {
			'nome': 'Tech Supply',
			'cnpj': '00.000.000/0001-00',
			'contato': '(11) 99999-9999',
			'email': 'contato@techsupply.com',
			'produto_principal': 'Monitores',
			'status': 'ATIVO',
			'observacoes': 'Entrega em 3 dias'
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Fornecedor.objects.count(), 1)

	def test_can_create_item(self):
		response = self.client.post(reverse('item_create'), {
			'nome': 'Mouse',
			'categoria': 'Periféricos',
			'localizacao': 'A1',
			'quantidade': 5,
			'status': 'DISPONIVEL',
			'valor': '120.00'
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Item.objects.count(), 1)

	def test_can_create_pedido(self):
		fornecedor = Fornecedor.objects.create(nome='Tech Supply')
		item = Item.objects.create(nome='Teclado', quantidade=10)
		response = self.client.post(reverse('novo_pedido'), {
			'fornecedor': fornecedor.pk,
			'item': item.pk,
			'quantidade': 3,
			'status': 'PENDENTE'
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Pedido.objects.count(), 1)
