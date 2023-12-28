from django_filters.rest_framework import FilterSet
from vms.models import PurchaseOrder


class VendorFilter(FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = ["vendor"]


class PurchaserFilter(FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = ["purchaser"]
