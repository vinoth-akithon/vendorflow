from django.urls import path
from vms import views
from rest_framework.routers import DefaultRouter


routers = DefaultRouter()
routers.register("vendors", views.VendorViewsSet, basename="vendor")
routers.register("purchasers", views.PurchaserViewset, basename="purchaser")
routers.register("purchase_orders", views.PurchaseOrderViewSet,
                 basename="purchase-order")

urlpatterns = []
urlpatterns += routers.urls
