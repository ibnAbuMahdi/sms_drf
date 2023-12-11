from .models import Item, InventoryRecord, SalesRecord, User, ItemPrice
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField

class UserSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	rank = serializers.CharField(source='type')

	class Meta:
		model = User
		fields = ('username', 'rank')

class ItemSerializer(serializers.ModelSerializer):
	"""
	name = CharField(required=True)
	quantity = IntegerField(source="stock", required=True,)
	unit = CharField(required=True)
	"""
	class Meta:
		model = Item
		fields = (
			'name',
			'stock',
			'unit'
		)

class ItemPriceSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.user.username')
	item_name = serializers.CharField(source='item.name')
	class Meta:
		model = ItemPrice
		fields=(
			'item_name',
			'price',
			'type',
			'username'
		)

class InventorySerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.user.username')
	item_name = serializers.CharField(source='item.name')
	item_price = serializers.FloatField(source='itemprice.price')
	shop_code = serializers.SlugField(source='shop.shop_code')
	class Meta:
		model = InventoryRecord
		fields = (
			'username',
			'item_name',
			'item_price',
			'quantity',
			'shop_code',
		)		


class SalesSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.user.username')
	item_name = serializers.CharField(source='item.name')
	item_price = serializers.FloatField(source='itemprice.price')
	shop_code = serializers.SlugField(source='shop.shop_code')
	class Meta:
		model = SalesRecord
		fields = (
			'username',
			'item_name',
			'item_price',
			'quantity',
			'shop_code',
		)		
