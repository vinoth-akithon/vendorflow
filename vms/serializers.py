import jsonschema
from django.utils import timezone
from rest_framework import serializers
from vms.models import PurchaseOrder, Purchaser, Vendor
from .validators import purchase_order_items_schema
from vms.signals import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "contact_details", "address"]


class VendorPermormanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["on_time_delivery_rate", "quality_rating_avg",
                  "average_response_time", "fulfillment_rate"]


class PurchaserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchaser
        fields = ["id", "name", "contact_details", "address"]


class AdminPurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ["id", "vendor", "purchaser", "items", "quantity", "status", 'quality_rating',
                  "ordered_date", "issued_date", "acknowledged_date", "expected_delivery_date", "actual_delivered_date"]


class PurchaserPurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ["id", "vendor", "items", "quantity", "status", 'quality_rating',
                  "ordered_date", "issued_date", "acknowledged_date", "expected_delivery_date", "actual_delivered_date"]


class VendorPurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ["id", "purchaser", "items", "quantity", "status", 'quality_rating',
                  "ordered_date", "issued_date", "acknowledged_date", "expected_delivery_date", "actual_delivered_date"]


class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["id", "vendor", "items"]

    def get_total_quantity(self, items: list[dict[str, str | int]]) -> int:
        return sum(map(lambda item: item["quantity"], items))

    def create(self, validated_data):
        validated_data["issued_date"] = timezone.now()
        validated_data["purchaser"] = self.context["purchaser"]
        validated_data["quantity"] = self.get_total_quantity(
            validated_data["items"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.acknowledged_date:
            raise serializers.ValidationError(
                "You cannot update this purchase order. This Purchase Order is in transist")
        validated_data["quantity"] = self.get_total_quantity(
            validated_data["items"])
        return super().update(instance, validated_data)

    def validate_items(self, value):
        try:
            jsonschema.validate(
                instance=value, schema=purchase_order_items_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise serializers.ValidationError(
                ["The 'items' field should be a JSON array must contain at least one object",
                 "Each object should contains 'item' and 'quantity' keys, like [{'item': 'x', 'quantity': 'y'}, ...]",
                 "'quantity' should greater than 1"])
        return value


class VendorAcknowledgePurchaseOrderSerializer(serializers.ModelSerializer):
    expected_delivery_date = serializers.DateTimeField()

    class Meta:
        model = PurchaseOrder
        fields = ["expected_delivery_date"]

    def update(self, instance, validated_data):
        validated_data["acknowledged_date"] = timezone.now()
        purchase_order = super().update(instance, validated_data)
        purchase_order_acknowledged.send_robust(
            self.__class__, purchase_order=purchase_order)
        return purchase_order


class VendorDeliveryPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = []

    def update(self, instance, validated_data):
        validated_data["actual_delivered_date"] = timezone.now()
        validated_data["status"] = "D"
        purchase_order = super().update(instance, validated_data)
        purchase_order_delivered.send_robust(
            self.__class__, purchase_order=purchase_order)
        purchase_order_status_changed.send_robust(
            self.__class__, purchase_order=purchase_order)
        return purchase_order


class QualityRatingPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["quality_rating"]

    def update(self, instance, validated_data):
        purchase_order = super().update(instance, validated_data)
        quality_rating_provided.send_robust(
            self.__class__, purchase_order=purchase_order)
        return purchase_order
