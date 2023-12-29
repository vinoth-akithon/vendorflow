from django.db import models
from django.conf import settings
from django.core import validators


class CommonInfo(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Vendor(CommonInfo):
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)


class Purchaser(CommonInfo):
    pass


class PurchaseOrder(models.Model):
    PO_CANCELED = "C"
    PO_PENDING = "P"
    PO_DELIVERED = "D"  # === Completed
    PO_STATUS = [
        (PO_PENDING, "Pending"),
        (PO_CANCELED, "Canceled"),
        (PO_DELIVERED, "Delivered")
    ]

    vendor = models.ForeignKey(
        Vendor, on_delete=models.DO_NOTHING, related_name="orders")
    purchaser = models.ForeignKey(
        Purchaser, on_delete=models.DO_NOTHING, related_name="orders")
    items = models.JSONField(null=False, blank=False)
    quantity = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1)])
    status = models.CharField(
        max_length=1, choices=PO_STATUS, default=PO_PENDING)
    quality_rating = models.FloatField(
        null=True, validators=[validators.MaxValueValidator(settings.RATING_BASE_VALUE), validators.MinValueValidator(0)])
    # When a purchaser placed an order
    ordered_date = models.DateTimeField(auto_now_add=True)
    # When an order assigned to the respecting vendor
    issued_date = models.DateTimeField(null=True)
    # When an order acknowledged by the vendor
    acknowledged_date = models.DateTimeField(null=True)
    # During acknowledgement, vendor committed to delivery date
    expected_delivery_date = models.DateTimeField(null=True)
    # When an order delivered to the purchacer
    actual_delivered_date = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.pk}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    recorded_data = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk}"
