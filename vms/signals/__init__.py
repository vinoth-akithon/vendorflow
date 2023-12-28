from django.dispatch import Signal


purchase_order_delivered = Signal()
quality_rating_provided = Signal()
purchase_order_acknowledged = Signal()
purchase_order_status_changed = Signal()
