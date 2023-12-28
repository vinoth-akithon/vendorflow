import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from vms.models import PurchaseOrder, Vendor, Purchaser
from vms.utils import AUTH_USER_MODEL_CLASS as User


@pytest.fixture
def bake_purchase_order():
    def do_bake_purchase_order(vendor, purchaser, **kwargs):
        return {
            "vendor": vendor,
            "purchaser": purchaser,
            "items": [{
                "item": "Smart Watch",
                "quantity": 10
            }, {
                "item": "Smart Phone",
                "quantity": 20
            }],
            "quantity": 2,
            **kwargs
        }
    return do_bake_purchase_order


@pytest.fixture
def bake_purchaser():
    def do_bake_purchaser(username):
        return {
            "username": username,
            "password": make_password("Success@2023"),
            "account_type": "P"
        }
    return do_bake_purchaser


@pytest.fixture
def bake_vendor():
    def do_bake_vendor(username):
        return {
            "username": username,
            "password": make_password("Success@2023"),
            "account_type": "P"
        }
    return do_bake_vendor


@pytest.fixture
def bake_vendor_profile():
    def do_bake_vendor_profile():
        return {
            "name": "Electronify",
            "contact_details": "7683489473",
            "address": "xyz"
        }
    return do_bake_vendor_profile


@pytest.fixture
def bake_purchaser_profile():
    def do_bake_purchaser_profile():
        return {
            "name": "Vinoth Kumar",
            "contact_details": "7683489473",
            "address": "xyz"
        }
    return do_bake_purchaser_profile


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authendicate_admin(api_client):
    def do_authendicate_admin():
        user = User(is_staff=True)
        api_client.force_authenticate(user=user)
    return do_authendicate_admin


@pytest.fixture
def authendicate_vendor(api_client):
    def do_authendicate_vendor():
        user = User(account_type="V")
        api_client.force_authenticate(user=user)
    return do_authendicate_vendor


@pytest.fixture
def authendicate_purchaser(api_client):
    def do_authendicate_parchaser():
        api_client.force_authenticate(user=User(account_type="P"))
    return do_authendicate_parchaser


@pytest.fixture
def custom_authendicate_vendor(api_client):
    def do_authendicate_vendor(vendor):
        user = User(account_type="V", pk=vendor.user_id)
        vendor = Vendor(pk=vendor.pk)
        user.vendor = vendor
        api_client.force_authenticate(user=user)
    return do_authendicate_vendor


@pytest.fixture
def custom_authendicate_purchaser(api_client):
    def do_authendicate_purchaser(purchaser):
        user = User(account_type="P", pk=purchaser.user_id)
        purchaser = Purchaser(pk=purchaser.pk)
        user.purchaser = purchaser
        api_client.force_authenticate(user=user)
    return do_authendicate_purchaser


@pytest.fixture
def create_purchaser_from_model():
    def do_create_purchaser_from_model(user_details):
        user = User.objects.create(**user_details)
        purchaser = Purchaser.objects.create(user_id=user.id)
        return purchaser
    return do_create_purchaser_from_model


@pytest.fixture
def create_vendor_from_model():
    def do_create_vendor_from_model(user_details):
        user = User.objects.create(**user_details)
        vendor = Vendor.objects.create(user_id=user.id)
        return vendor
    return do_create_vendor_from_model


@pytest.fixture
def create_purchase_order_from_model():
    def do_create_purchase_order_from_model(order_details):
        purchase_order = PurchaseOrder.objects.create(**order_details)
        return purchase_order
    return do_create_purchase_order_from_model
