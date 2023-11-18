from django.db import models
from django.contrib.auth.models import User as Usr

from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)
class User(models.Model):
    user = models.OneToOneField(Usr, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=(('SM', 'Shop Manager'), ('SA', 'Shop Assistant')))


class Item(
    TimeStampedModel,
    ActivatorModel ,
    TitleSlugDescriptionModel,
    Model):

    """
    ecommerce.Item
    Stores a single item entry for our shop
    """

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ["id"]

    def __str__(self):
        return self.title
    
    stock = models.IntegerField(default=1)
    unit = models.CharField(max_length=20)


    def manage_stock(self, qty):
        #used to reduce Item stock
        new_stock = self.stock - int(qty)
        self.stock = new_stock
        self.save()

    def check_stock(self, qty):
        #used to check if order quantity exceeds stock levels
        if int(qty) > self.stock:
            return False
        return True

    def place_order(self, user, qty):
        #used to place an order
        if self.check_stock(qty):
            record = SalesRecord.objects.create(
                item = self, 
                quantity = qty, 
                user = user,
                itemprice = self.get_price('s'))
            self.manage_stock(qty)
            return record
        else:
            return None

    def get_price(self, typ):
        price = ItemPrice.objects.filter(item=self, type=typ).order_by('created').first()
        return price

    def manage_inventory(self, user, qty):
        if int(qty) + self.stock >= 0:
            record = InventoryRecord.objects.create(
                user=user,
                item=self,
                itemprice=self.get_price('c'),
                quantity=qty)
            self.manage_stock(-1*qty)
            return record
        else:
            return None


class ItemPrice(
    TimeStampedModel,
    ActivatorModel ,
    Model):

    class Meta:
        verbose_name = 'Item_price'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    price = models.FloatField()
    type = models.CharField(max_length=1, choices=(('s', 'sale'), ('c', 'cost')))


class SalesRecord(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    """
    ecommerce.Order
    Stores a single order entry, related to :model:`ecommerce.Item` and
    :model:`auth.User`.
    """
    class Meta:
        verbose_name = 'SalesRecord'
        verbose_name_plural = 'SalesRecords'
        ordering = ["id"]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    itemprice = models.ForeignKey(ItemPrice, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username} - {self.item.title}'


class InventoryRecord(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    """
    ecommerce.Order
    Stores a single order entry, related to :model:`ecommerce.Item` and
    :model:`auth.User`.
    """
    class Meta:
        verbose_name = 'InventoryRecord'
        verbose_name_plural = 'InventoryRecords'
        ordering = ["id"]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    itemprice = models.ForeignKey(ItemPrice, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.item.title}'
