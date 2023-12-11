from django.contrib import admin
from django.urls import include
from core import views as core_views
from sms import views as sms_views
from ecommerce import views as ecommerce_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sms import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'sales', views.SalesViewSet, basename='sale')
router.register(r'inventories', views.InventoryViewSet, basename='inventory')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]


urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('contact/', core_views.ContactAPIView.as_view()),
    path('api-token-auth/', obtain_auth_token),
    path('item/', sms_views.handle_items, name='handle_items'),
    path('item/<uuid:id>/', sms_views.get_items, name='get_item'),
    path('inventory/', sms_views.handle_inventory, name='handle_inventory'),
    path('sales/', sms_views.handle_sales, name='handle_sales'),
    path('inventory/<uuid:id>/', sms_views.inventory_record, name='get_inventory_record'),
    path('sales/<uuid:id>/', sms_views.sales_record, name='get_sales_record'),
    path('itemprice/', sms_views.set_itemprice, name='set_itemprice'),
    path('item/sales/', sms_views.create_sale, name='create_sale'),
    path('item/inventory/<uuid:id>', sms_views.create_inventory, name='create_inventory'),
]
