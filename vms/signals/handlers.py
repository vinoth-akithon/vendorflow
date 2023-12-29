from django.dispatch import receiver
from django.db.models import Count, Sum, Case, When, ExpressionWrapper, F, Avg
from django.db.models import fields
from django.utils import timezone
from vms.models import PurchaseOrder
from vms.utils import *
from vms.signals import *


@receiver(purchase_order_delivered)
def on_time_delivery_rate(sender, **kwargs):
    purchase_order = kwargs["purchase_order"]
    vendor = purchase_order.vendor
    aggregated_result = PurchaseOrder.objects \
        .filter(vendor=vendor, status="D") \
        .aggregate(
            total_completed_orders=Count('id'),
            total_completed_orders_ontime=Sum(Case(When(
                expected_delivery_date__date__gte=timezone.now().date(), then=1), default=0))
        )

    if aggregated_result["total_completed_orders"]:
        delivery_rate = calculate_on_time_delivery_rate(
            aggregated_result["total_completed_orders"], aggregated_result["total_completed_orders_ontime"])
        vendor.on_time_delivery_rate = delivery_rate
        vendor.save()


@receiver(quality_rating_provided)
def purhase_order_quality_rating(sender, **kwargs):
    purchase_order = kwargs["purchase_order"]
    vendor = purchase_order.vendor
    aggregated_result = PurchaseOrder.objects \
        .filter(vendor=vendor, status="D", quality_rating__isnull=False) \
        .aggregate(
            total_completed_orders=Count('id'),
            total_completed_orders_ratings=Sum("quality_rating")
        )

    if aggregated_result["total_completed_orders"]:
        quality_rate = calculate_quality_ratings_average(
            aggregated_result["total_completed_orders"], aggregated_result["total_completed_orders_ratings"])
        vendor.quality_rating_avg = quality_rate
        vendor.save()


@receiver(purchase_order_acknowledged)
def average_response_time(sender, **kwargs):
    purchase_order = kwargs["purchase_order"]
    vendor = purchase_order.vendor
    average_response_time = PurchaseOrder.objects \
        .annotate(
            response_time=ExpressionWrapper(F('acknowledged_date') - F('issued_date'), output_field=fields.IntegerField())) \
        .aggregate(average_response_time=Avg('response_time')
                   )

    average_response_time_in_days = calculate_average_response_time_in_days(
        average_response_time["average_response_time"])

    vendor.average_response_time = average_response_time_in_days
    vendor.save()


@receiver(purchase_order_status_changed)
def fulfillment_rate(sender, **kwargs):
    purchase_order = kwargs["purchase_order"]
    vendor = purchase_order.vendor
    aggregated_result = PurchaseOrder.objects \
        .filter(vendor=vendor) \
        .aggregate(
            total_issued_orders=Count('id'),
            total_completed_orders=Sum(Case(When(
                status="D", then=1), default=0))
        )

    if aggregated_result["total_issued_orders"]:
        fulfillment_rate = calculate_fulfillment_rate(
            aggregated_result["total_issued_orders"],
            aggregated_result["total_completed_orders"])
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()
