import pytest
from rest_framework import status
from django.contrib.auth.hashers import make_password


@pytest.fixture
def list_vendors(api_client):
    def do_list_vendors():
        return api_client.get("/api/vendors/")
    return do_list_vendors


@pytest.fixture
def retrieve_vendor(api_client):
    def do_retrieve_vendor(vendor_id):
        return api_client.get(f"/api/vendors/{vendor_id}/")
    return do_retrieve_vendor


@pytest.fixture
def update_vendor(api_client):
    def do_update_vendor(vendor_id, request_body):
        return api_client.put(f"/api/vendors/{vendor_id}/", data=request_body)
    return do_update_vendor


@pytest.fixture
def retrieve_me_vendor(api_client):
    def do_retrieve_me_vendor():
        return api_client.get(f"/api/vendors/me/")
    return do_retrieve_me_vendor


@pytest.fixture
def update_me_vendor(api_client):
    def do_update_me_vendor(data):
        return api_client.put(f"/api/vendors/me/", data=data)
    return do_update_me_vendor


@pytest.fixture
def retrieve_performance_matrix(api_client):
    def do_retrieve_performance_matrix(vendor_id):
        return api_client.get(f"/api/vendors/{vendor_id}/performance/")
    return do_retrieve_performance_matrix


@pytest.mark.django_db
class TestListVendor:
    def test_if_anonymous_user_access_vendors_list_return_401(self, list_vendors):
        response = list_vendors()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_vendor_access_vendors_list_return_200(self, list_vendors, authendicate_vendor):
        authendicate_vendor()

        response = list_vendors()

        assert response.status_code == status.HTTP_200_OK

    def test_if_purchaser_access_vendors_list_return_200(self, list_vendors, authendicate_purchaser):
        authendicate_purchaser()

        response = list_vendors()

        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_access_vendors_list_return_200(self, list_vendors, authendicate_admin):
        authendicate_admin()

        response = list_vendors()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetriveVendor:
    def test_if_anonymous_user_access_vendor_details_return_401(self, create_vendor_from_model, retrieve_vendor, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))

        response = retrieve_vendor(vendor.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_vendor_access_vendor_details_return_200(self, authendicate_vendor, create_vendor_from_model, retrieve_vendor, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        authendicate_vendor()

        response = retrieve_vendor(vendor.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_purchaser_access_vendor_details_return_200(self, authendicate_purchaser, create_vendor_from_model, retrieve_vendor, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        authendicate_purchaser()

        response = retrieve_vendor(vendor.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_access_vendor_details_return_200(self, authendicate_admin, create_vendor_from_model, retrieve_vendor, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        authendicate_admin()

        response = retrieve_vendor(vendor.id)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveMeVendor:

    def test_if_anonymous_user_return_401(self, retrieve_me_vendor):
        response = retrieve_me_vendor()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_return_403(self, retrieve_me_vendor, create_purchaser_from_model,  bake_purchaser, custom_authendicate_purchaser):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        custom_authendicate_purchaser(purchaser)

        response = retrieve_me_vendor()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_return_403(self, retrieve_me_vendor, authendicate_admin):
        authendicate_admin()

        response = retrieve_me_vendor()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_return_200(self, retrieve_me_vendor, custom_authendicate_vendor, create_vendor_from_model, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        custom_authendicate_vendor(vendor)

        response = retrieve_me_vendor()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdateMeVendor:

    def test_if_anonymous_user_return_401(self, update_me_vendor, bake_vendor_profile):
        request_body = bake_vendor_profile()
        response = update_me_vendor(request_body)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_purchaser_return_403(self, update_me_vendor, create_purchaser_from_model, bake_purchaser, custom_authendicate_purchaser, bake_vendor_profile):
        purchaser = create_purchaser_from_model(bake_purchaser("purchaser-1"))
        custom_authendicate_purchaser(purchaser)
        request_body = bake_vendor_profile()

        response = update_me_vendor(request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_return_403(self, update_me_vendor, authendicate_admin, bake_vendor_profile):
        authendicate_admin()
        request_body = bake_vendor_profile()

        response = update_me_vendor(request_body)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_vendor_return_200(self, update_me_vendor, custom_authendicate_vendor, create_vendor_from_model, bake_vendor, bake_vendor_profile):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        custom_authendicate_vendor(vendor)

        request_body = bake_vendor_profile()
        response = update_me_vendor(request_body)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrievePerformanceMatrixVendor:
    def test_if_anonymous_user_return_401(self, create_vendor_from_model, retrieve_performance_matrix, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))

        response = retrieve_performance_matrix(vendor.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_vendor_return_200(self, authendicate_vendor, create_vendor_from_model, retrieve_performance_matrix, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        authendicate_vendor()

        response = retrieve_performance_matrix(vendor.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_purchaser_return_200(self, authendicate_purchaser, create_vendor_from_model, retrieve_performance_matrix, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        authendicate_purchaser()

        response = retrieve_performance_matrix(vendor.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_access_vendor_details_return_200(self, authendicate_admin, create_vendor_from_model, retrieve_performance_matrix, bake_vendor):
        vendor = create_vendor_from_model(bake_vendor("vendor-1"))
        authendicate_admin()

        response = retrieve_performance_matrix(vendor.id)

        assert response.status_code == status.HTTP_200_OK
