import json
import pytest
from rest_framework import status
from django.utils import timezone

from vms.models import PurchaseOrder


@pytest.fixture
def list_purchase_orders(api_client):
    def do_list_purchase_orders():
        return api_client.get("/api/purchase_orders/")
    return do_list_purchase_orders


@pytest.fixture
def retrieve_purchase_order(api_client):
    def do_retrieve_purchase_order(po_id):
        return api_client.get(f"/api/purchase_orders/{po_id}/")
    return do_retrieve_purchase_order


@pytest.fixture
def update_purchase_order(api_client):
    def do_update_purchase_order(po_id, data):
        return api_client.put(f"/api/purchase_orders/{po_id}/", data=json.dumps(data), content_type="application/json")
    return do_update_purchase_order


@pytest.fixture
def cancel_purchase_order(api_client):
    def do_cancel_purchase_order(po_id):
        return api_client.delete(f"/api/purchase_orders/{po_id}/")
    return do_cancel_purchase_order


@pytest.fixture
def create_purchase_order(api_client):
    def do_create_purchase_order(data):
        return api_client.post("/api/purchase_orders/", data=json.dumps(data), content_type='application/json')
    return do_create_purchase_order


@pytest.fixture
def acknowledge_purchase_order(api_client):
    def do_acknowledge_purchase_order(po_id, data):
        return api_client.put(f"/api/purchase_orders/{po_id}/acknowledge/", data=data)
    return do_acknowledge_purchase_order


@pytest.fixture
def delivery_purchase_order(api_client):
    def do_delivery_purchase_order(po_id):
        return api_client.put(f"/api/purchase_orders/{po_id}/delivery/")
    return do_delivery_purchase_order


@pytest.fixture
def rating_purchase_order(api_client):
    def do_rating_purchase_order(po_id, data):
        return api_client.put(f"/api/purchase_orders/{po_id}/rating/", data=data)
    return do_rating_purchase_order


@pytest.mark.django_db
class TestListPurchaseOrder:

    def test_if_anonymous_return_401(self, list_purchase_orders, create_purchaser_from_model, bake_purchaser, create_vendor_from_model, bake_vendor, create_purchase_order_from_model, bake_purchase_order):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))

        response = list_purchase_orders()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_return_their_purchase_orders_and_200(self, list_purchase_orders, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser2))
        purchase_order3 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser1))
        custom_authendicate_purchaser(purchaser1)

        response = list_purchase_orders()
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == 2

    def test_if_vendor_return_their_issued_purchase_orders_and_200(self, list_purchase_orders, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser2))
        purchase_order3 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        custom_authendicate_vendor(vendor1)

        response = list_purchase_orders()
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == 2

    def test_if_admin_return_all_purchase_order_and_200(self, list_purchase_orders, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser2))
        purchase_order3 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        authendicate_admin()

        response = list_purchase_orders()
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == 3


@pytest.mark.django_db
class TestCreatePurchaseOrder:

    def test_if_anonymous_user_return_401(self, create_purchase_order, create_vendor_from_model, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 10
            }, {
                "item": "Smart Phone",
                "quantity": 20
            }]
        }

        response = create_purchase_order(request_body)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_return_created_order_and_201(self, create_purchase_order, create_vendor_from_model, create_purchaser_from_model, bake_vendor, bake_purchaser, custom_authendicate_purchaser):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 10
            }, {
                "item": "Smart Phone",
                "quantity": 20
            }]
        }
        custom_authendicate_purchaser(purchaser)

        response = create_purchase_order(request_body)
        response_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert response_data["vendor"] == vendor.pk

    def test_if_vendor_return_403(self, create_purchase_order, create_vendor_from_model, bake_vendor, custom_authendicate_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 10
            }, {
                "item": "Smart Phone",
                "quantity": 20
            }]
        }
        custom_authendicate_vendor(vendor)

        response = create_purchase_order(request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_return_403(self, create_purchase_order, create_vendor_from_model, bake_vendor, authendicate_admin):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 10
            }, {
                "item": "Smart Phone",
                "quantity": 20
            }]
        }
        authendicate_admin()

        response = create_purchase_order(request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRetrivePurchaseOrder:
    def test_if_anonymous_return_401(self, retrieve_purchase_order, create_purchaser_from_model, bake_purchaser, create_vendor_from_model, bake_vendor, create_purchase_order_from_model, bake_purchase_order):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))

        response = retrieve_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_requesting_their_PO_return_that_PO_and_200(self, retrieve_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        custom_authendicate_purchaser(purchaser)

        response = retrieve_purchase_order(purchase_order.pk)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["id"] == purchase_order.pk

    def test_if_purchaser_requesting_other_purchaser_PO_return_404(self, retrieve_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser2))
        custom_authendicate_purchaser(purchaser1)

        response = retrieve_purchase_order(purchase_order2.pk)
        response_data = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vendor_requesting_their_issued_PO_return_that_PO_200(self, retrieve_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser))
        custom_authendicate_vendor(vendor1)

        response = retrieve_purchase_order(purchase_order1.pk)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data["id"] == purchase_order1.pk

    def test_if_vendor_requesting_other_vendor_PO_return_404(self, retrieve_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser))
        custom_authendicate_vendor(vendor1)

        response = retrieve_purchase_order(purchase_order2.pk)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_requesting_any_PO_return_200(self, retrieve_purchase_order, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        authendicate_admin()

        response = retrieve_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdatePurchaseOrder:

    def test_if_anonymous_user_return_401(self, update_purchase_order, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 100
            }]
        }

        response = update_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_update_thier_PO_return_200(self, update_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 100
            }]
        }
        custom_authendicate_purchaser(purchaser)

        response = update_purchase_order(purchase_order.pk, request_body)
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data["items"]) == 1
        assert response_data["items"] == request_body["items"]

    def test_if_purchaser_update_others_PO_return_404(self, update_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser2))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 100
            }]
        }
        custom_authendicate_purchaser(purchaser1)

        response = update_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vendor_update_their_issued_PO_return_403(self, update_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 100
            }]
        }
        custom_authendicate_vendor(vendor)

        response = update_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_update_others_issued_PO_return_403(self, update_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser))
        request_body = {
            "vendor": vendor2.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 100
            }]
        }
        custom_authendicate_vendor(vendor1)

        response = update_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_update_PO_return_403(self, update_purchase_order, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {
            "vendor": vendor.pk,
            "items": [{
                "item": "Smart Watch",
                "quantity": 100
            }]
        }
        authendicate_admin()

        response = update_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCancelPurchaseOrder:

    def test_if_anonymous_user_return_401(self, cancel_purchase_order, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))

        response = cancel_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_cancel_their_PO_that_not_acknowledged_and_not_delivered_return_204(self, cancel_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        custom_authendicate_purchaser(purchaser)

        response = cancel_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_purchaser_cancel_their_PO_that_acknowledged_and_delivered_return_400(self, cancel_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now(), actual_delivered_date=timezone.now()))
        custom_authendicate_purchaser(purchaser)

        response = cancel_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_purchaser_cancel_their_PO_that_acknowledged_and_not_delivered_return_400(self, cancel_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now()))
        custom_authendicate_purchaser(purchaser)

        response = cancel_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_purchaser_cancel_others_PO_return_404(self, cancel_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser2))
        custom_authendicate_purchaser(purchaser1)

        response = cancel_purchase_order(purchase_order2.pk)

    def test_if_vendor_cancel_their_issued_PO_return_403(self, cancel_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        custom_authendicate_vendor(vendor)

        response = cancel_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_cancel_others_issued_PO_return_403(self, cancel_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser))
        custom_authendicate_vendor(vendor1)

        response = cancel_purchase_order(purchase_order2.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_cancel_PO_return_403(self, cancel_purchase_order, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))

        authendicate_admin()

        response = cancel_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestAckowledgePurchaseOrder:

    def test_if_anonymous_user_acknowledge_PO_return_401(self, acknowledge_purchase_order, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {
            "expected_delivery_date": timezone.now()
        }
        response = acknowledge_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_acknowledge_PO_return_403(self, acknowledge_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {"expected_delivery_date": timezone.now()}
        custom_authendicate_purchaser(purchaser)

        response = acknowledge_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_acknowledge_PO_return_403(self, acknowledge_purchase_order, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {"expected_delivery_date": timezone.now()}
        authendicate_admin()

        response = acknowledge_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_acknowledge_their_PO_when_not_acknowledged_and_pending_state_return_200(self, acknowledge_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser))
        request_body = {"expected_delivery_date": timezone.now()}
        custom_authendicate_vendor(vendor)

        response = acknowledge_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_200_OK

    def test_if_vendor_acknowledge_their_PO_when_acknowledged_and_pending_state_return_400(self, acknowledge_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, expected_delivery_date=timezone.now(), acknowledged_date=timezone.now()))
        request_body = {"expected_delivery_date": timezone.now()}
        custom_authendicate_vendor(vendor)

        response = acknowledge_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_vendor_acknowledge_their_PO_when_acknowledged_and_not_pending_state_return_400(self, acknowledge_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, expected_delivery_date=timezone.now(), acknowledged_date=timezone.now(), status="D"))
        request_body = {"expected_delivery_date": timezone.now()}
        custom_authendicate_vendor(vendor)

        response = acknowledge_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_vendor_acknowledge_others_PO_when_not_acknowledged_and_pending_state_return_404(self, acknowledge_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser))

        request_body = {"expected_delivery_date": timezone.now()}
        custom_authendicate_vendor(vendor1)

        response = acknowledge_purchase_order(purchase_order2.pk, request_body)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeliveryPurchaseOrder:

    def test_if_anonymous_user_delivery_PO_return_401(self, delivery_purchase_order, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="P"))

        response = delivery_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_delivery_PO_return_403(self, delivery_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="P"))
        custom_authendicate_purchaser(purchaser)

        response = delivery_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_delivery_PO_return_403(self, delivery_purchase_order, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="P"))

        authendicate_admin()

        response = delivery_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_delivery_their_PO_when_acknowledged_and_pending_state_return_200(self, delivery_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="P"))
        custom_authendicate_vendor(vendor)

        response = delivery_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_if_vendor_delivery_their_PO_when_not_acknowledged_and_pending_state_return_400(self, delivery_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, status="P"))
        custom_authendicate_vendor(vendor)

        response = delivery_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_vendor_delivery_their_PO_when_acknowledged_and_not_pending_state_return_400(self, delivery_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="D"))
        custom_authendicate_vendor(vendor)

        response = delivery_purchase_order(purchase_order.pk)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_vendor_delivery_others_PO_when_acknowledged_and_pending_state_return_404(self, delivery_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="P"))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser, acknowledged_date=timezone.now(), expected_delivery_date=timezone.now(), status="P"))

        custom_authendicate_vendor(vendor1)

        response = delivery_purchase_order(purchase_order2.pk)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRatingPurchaseOrder:

    def test_if_anonymous_user_rating_PO_return_401(self, rating_purchase_order, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, status="D"))
        request_body = {"quality_rating": 5}

        response = rating_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_vendor_rating_PO_return_403(self, rating_purchase_order, custom_authendicate_vendor, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, status="D"))
        request_body = {"quality_rating": 5}
        custom_authendicate_vendor(vendor)

        response = rating_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_rating_PO_return_403(self, rating_purchase_order, authendicate_admin, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, status="D"))
        request_body = {"quality_rating": 5}
        authendicate_admin()

        response = rating_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_purchaser_rating_their_PO_when_delivered_return_200(self, rating_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, status="D"))
        request_body = {"quality_rating": 5}
        custom_authendicate_purchaser(purchaser)

        response = rating_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_200_OK

    def test_if_purchaser_rating_their_PO_when_not_delivered_return_400(self, rating_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser, status="P"))
        request_body = {"quality_rating": 5}
        custom_authendicate_purchaser(purchaser)

        response = rating_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_purchaser_rating_others_PO_when_delivered_return_404(self, rating_purchase_order, custom_authendicate_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        purchase_order = create_purchase_order_from_model(
            bake_purchase_order(vendor, purchaser2, status="D"))
        request_body = {"quality_rating": 5}
        custom_authendicate_purchaser(purchaser1)

        response = rating_purchase_order(purchase_order.pk, request_body)

        assert response.status_code == status.HTTP_404_NOT_FOUND
