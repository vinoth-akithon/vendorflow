from django.conf import settings
from django.apps import apps

AUTH_USER_MODEL_CLASS = apps.get_model(
    *settings.AUTH_USER_MODEL.rsplit(".", 1))


def calculate_on_time_delivery_rate(total_completed_orders: int, total_completed_orders_ontime: int) -> float:
    return (total_completed_orders_ontime/total_completed_orders) * settings.RATING_BASE_VALUE


def calculate_fulfillment_rate(total_issued_orders: int, total_completed_orders: int) -> float:
    return (total_completed_orders/total_issued_orders) * settings.RATING_BASE_VALUE


def calculate_quality_ratings_average(total_completed_orders: int, total_completed_orders_ratings: int) -> float:
    return (total_completed_orders_ratings/total_completed_orders)


def calculate_average_response_time_in_days(average_repsponse_time_in_microsecond: float) -> float:
    return format((average_repsponse_time_in_microsecond/((10**6) * 60 * 60 * 24)), ".1f")
