from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from django.forms import model_to_dict
import json
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed as not_allowed
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import status
# Create your views here.

def handle_items(request):
    # if method is POST
    if request.method == 'POST':
        # handle item creation
        data = JSONParser().parse(request)
        serializer = ItemSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # elif method is GET
    elif request.method == 'GET':    
        # return all items
        items = Item.objects.all()
        data = ItemSerializer(items, many=True).data
        return JsonResponse(data, safe=False)
    # else:
    else:
        # return error
        return not_allowed(['GET', 'POST'])


def get_items(request, id):
    item = get_object_or_404(Item, id=id)
    return JsonResponse(ItemSerializer(item).data, safe=False)


def handle_inventory(request):
    # if method is POST
    if request.method == 'POST':
        # get records and filter based on POST input creation
        params = JSONParser().parse(request)
        qr = get_list_or_404(InventoryRecord, item__id=params.get('item'), created__range=[params.get('begin'), params.get('end')])
        return JsonResponse(qr, safe=False)
    # elif method is GET
    elif request.method == 'GET':
        # return all records
        items = get_list_or_404(InventoryRecord)
        return JsonResponse(items, safe=False)
    
    # else:
    else:
        # return error
        return not_allowed(['GET', 'POST'])


def handle_sales(request):
    # if method is POST
    if request.method == 'POST':
        # get records and filter based on POST input creation
        params = JSONParser().parse(request)
        qr = get_list_or_404(SalesRecord, item__id=params.get('item'), created__range=[params.get('begin'), params.get('end')])
        return JsonResponse(qr, safe=False)
    # elif method is GET
    elif request.method == 'GET':
        # return all records
        items = get_list_or_404(SalesRecord)
        return JsonResponse(items, safe=False)
    
    # else:
    else:
        # return error
        return not_allowed(['GET', 'POST'])

def inventory_record(request, id):
    item = get_object_or_404(InventoryRecord, id=id)
    if request.method == 'GET':
        dct_obj = model_to_dict(item)
        js = json.dumps(dct_obj)
        return JsonResponse(js, safe=False)
    elif request.method == 'DELETE':
        item.delete()
        return HttpResponse(status=204)



def sales_record(request, id):
    item = get_object_or_404(SalesRecord, id=id)
    if request.method == 'GET':
        dct_obj = model_to_dict(item)
        js = json.dumps(dct_obj)
        return JsonResponse(js, safe=False)
    elif request.method == 'DELETE':
        item.delete()
        return HttpResponse(status=204)

def set_itemprice(request):
    # if method is POST
    if request.method == 'POST':
        # validate item id
        js = JSONParser().parse(request)
        item = get_object_or_404(Item, item__id=js.get('item_id'))
        price = js.get('price')
        typ = js.get('type')
        if item:
            # create item price
            itemprice = ItemPrice.objects.create(
                item=item,
                user=User,
                price=price,
                type=typ
            )
            itemprice.save()

def create_sale(request):
    params = JSONParser().parse(request)
    item = get_object_or_404(id=params.get('id'))
    item.place_order(User, params.get('qty'))
    return item

def create_inventory(request):

    params = JSONParser().parse(request)
    item = get_object_or_404(id=params.get('id'))
    item.manage_inventory(User, params.get('qty'))
    return item



class UserViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        staff = self.get_object()
        mgr = self.queryset.filter(type='M').first()
        # only manager can assign shop to others
        if (staff == mgr and self.request.data.get('shop_code')) or (staff != mgr and not self.request.data.get('shop_code')):
            serializer.save()

    def perform_create(self, serializer):
        typ = self.request.data.get('type')
        m = self.queryset.get(type='M')
        if typ != 'M' or (typ == 'M' and not m):
            serializer.save()
            


class ItemViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        shop = Shop.objects.get(id=self.request.data.get('shop_id'))
        serializer.save(user=self.request.user, shop=shop)
    
class SalesViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = SalesRecord.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        shop = Shop.objects.get(id=self.request.data.get('shop_id'))
        itemprice = ItemPrice.objects.get(id=self.request.data.get('itemprice_id'))
        item = Item.objects.get(id=self.request.data.get('item_id'))
        serializer.save(user=self.request.user, shop=shop, itemprice=itemprice, item=item)

class InventoryViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = InventoryRecord.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        shop = Shop.objects.get(id=self.request.data.get('shop_id'))
        itemprice = ItemPrice.objects.get(id=self.request.data.get('itemprice_id'))
        item = Item.objects.get(id=self.request.data.get('item_id'))
        serializer.save(user=self.request.user, shop=shop, itemprice=itemprice, item=item)
