import pytest
from rest_framework import status


@pytest.fixture
def list_purchasers(api_client):
    def do_list_purchasers():
        return api_client.get("/api/purchasers/")
    return do_list_purchasers


@pytest.fixture
def retrieve_purchaser(api_client):
    def do_retrieve_purchaser(purchaser_id):
        return api_client.get(f"/api/purchasers/{purchaser_id}/")
    return do_retrieve_purchaser


@pytest.fixture
def retrieve_me_purchaser(api_client):
    def do_retrieve_me_purchaser():
        return api_client.get(f"/api/purchasers/me/")
    return do_retrieve_me_purchaser


@pytest.fixture
def update_me_purchaser(api_client):
    def do_update_me_purchaser(data):
        return api_client.put(f"/api/purchasers/me/", data=data)
    return do_update_me_purchaser


@pytest.mark.django_db
class TestListPurchaser:

    def test_if_anonymous_user_return_401(self, list_purchasers):
        response = list_purchasers()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_access_puchasers_list_return_403(self, list_purchasers, authendicate_purchaser):
        authendicate_purchaser()

        response = list_purchasers()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_access_their_puchasers_list_return_200(self, list_purchasers, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor, custom_authendicate_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        purchaser3 = create_purchaser_from_model(bake_purchaser("purchaser-3"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser2))
        purchase_order3 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser3))
        custom_authendicate_vendor(vendor1)

        response = list_purchasers()
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == 2

    def test_if_admin_access_all_puchasers_list_return_200(self, list_purchasers, authendicate_admin, create_purchaser_from_model, bake_purchaser):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))

        authendicate_admin()

        response = list_purchasers()
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_data) == 2


@pytest.mark.django_db
class TestRetrievePurchaser:

    def test_if_anonymous_user_return_401(self, retrieve_purchaser, create_purchaser_from_model, bake_purchaser):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        response = retrieve_purchaser(purchaser.pk)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_return_403(self, retrieve_purchaser, authendicate_purchaser, create_purchaser_from_model, bake_purchaser):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        authendicate_purchaser()

        response = retrieve_purchaser(purchaser.pk)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_access_their_purchaser_details_return_200(self, retrieve_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor, custom_authendicate_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser2))
        custom_authendicate_vendor(vendor1)

        response = retrieve_purchaser(purchaser1.pk)

        assert response.status_code == status.HTTP_200_OK

    def test_if_vendor_access_other_vendors_puchaser_details_return_404(self, retrieve_purchaser, create_purchaser_from_model, create_vendor_from_model, create_purchase_order_from_model, bake_purchase_order, bake_purchaser, bake_vendor, custom_authendicate_vendor):
        purchaser1 = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        purchaser2 = create_purchaser_from_model(bake_purchaser("purchaser-2"))
        purchaser3 = create_purchaser_from_model(bake_purchaser("purchaser-3"))
        vendor1 = create_vendor_from_model(bake_vendor("vendor-1"))
        vendor2 = create_vendor_from_model(bake_vendor("vendor-2"))
        purchase_order1 = create_purchase_order_from_model(
            bake_purchase_order(vendor1, purchaser1))
        purchase_order2 = create_purchase_order_from_model(
            bake_purchase_order(vendor2, purchaser2))
        custom_authendicate_vendor(vendor1)

        response = retrieve_purchaser(purchaser3.pk)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_access_all_puchaser_details_return_200(self, retrieve_purchaser, authendicate_admin, create_purchaser_from_model, bake_purchaser):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))

        authendicate_admin()

        response = retrieve_purchaser(purchaser.pk)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveMePurchaser:

    def test_if_anonymous_user_return_401(self, retrieve_me_purchaser):
        response = retrieve_me_purchaser()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_vendor_return_403(self, retrieve_me_purchaser, custom_authendicate_vendor, create_vendor_from_model, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        custom_authendicate_vendor(vendor)

        response = retrieve_me_purchaser()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_return_403(self, retrieve_me_purchaser, authendicate_admin):
        authendicate_admin()

        response = retrieve_me_purchaser()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_purchaser_return_200(self, retrieve_me_purchaser, create_purchaser_from_model,  bake_purchaser, custom_authendicate_purchaser):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        custom_authendicate_purchaser(purchaser)

        response = retrieve_me_purchaser()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdateMePurchaser:

    def test_if_anonymous_user_return_401(self, update_me_purchaser, bake_purchaser_profile):
        request_body = bake_purchaser_profile()
        response = update_me_purchaser(request_body)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_vendor_return_403(self, update_me_purchaser, custom_authendicate_vendor, create_vendor_from_model, bake_vendor, bake_purchaser_profile):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        custom_authendicate_vendor(vendor)

        request_body = bake_purchaser_profile()
        response = update_me_purchaser(request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_return_403(self, update_me_purchaser, authendicate_admin, bake_purchaser_profile):
        authendicate_admin()

        request_body = bake_purchaser_profile()
        response = update_me_purchaser(request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_purchaser_return_200(self, update_me_purchaser, create_purchaser_from_model, bake_purchaser, custom_authendicate_purchaser, bake_purchaser_profile):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        custom_authendicate_purchaser(purchaser)

        request_body = bake_purchaser_profile()
        response = update_me_purchaser(request_body)

        assert response.status_code == status.HTTP_200_OK
