from django.conf import settings
from django.apps import apps
from django.contrib.auth.hashers import make_password
from rest_framework import status
import pytest


@pytest.fixture
def register_user(api_client) -> callable:
    def do_register_user(user_detail: dict[str, str]):
        return api_client.post("/api/auth/register/", user_detail)
    return do_register_user


@pytest.fixture
def login_user(api_client) -> callable:
    def do_login_user(user_detail: dict[str, str]):
        return api_client.post("/api/auth/login/", user_detail)
    return do_login_user


@pytest.fixture
def create_user() -> callable:
    def do_create_user(user_details: dict[str, str]):
        User = apps.get_model(*settings.AUTH_USER_MODEL.rsplit(".", 1))
        user = User.objects.create(**user_details)
        return user
    return do_create_user


@pytest.mark.django_db
class TestUserRegistration:

    def test_if_parchaser_registeration_success_and_return_201(self, register_user):
        data = {
            "username": "parchaser-1",
            "password": "Success@2023",
            "account_type": "P",
            "name": "parchaser-1",
            "contact_details": "",
            "address": ""

        }

        response = register_user(data)
        response_data = response.json()
        data.pop("password")

        assert response.status_code == status.HTTP_201_CREATED
        assert data == response_data

    def test_if_vendor_registeration_success_and_return_201(self, register_user):
        data = {
            "username": "vendor-1",
            "password": "Success@2023",
            "account_type": "V",
            "name": "vendor-1",
            "contact_details": "",
            "address": ""
        }

        response = register_user(data)
        response_data = response.json()
        data.pop("password")

        assert response.status_code == status.HTTP_201_CREATED
        assert data == response_data

    def test_if_vendor_registeration_with_duplicate_username_and_return_400(self, register_user):
        data = {
            "username": "vendor-1",
            "password": "Success@2023",
            "account_type": "V",
            "name": "vendor-1",
            "contact_details": "",
            "address": ""
        }
        register_user(data)

        response = register_user(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_vendor_registeration_with_invalid_account_type_and_return_400(self, register_user):
        data = {
            "username": "vendor-1",
            "password": "Success@2023",
            "account_type": "Z",
            "name": "vendor-1",
            "contact_details": "",
            "address": ""
        }

        response = register_user(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db()
class TestUserLogin:
    def test_if_vendor_login_success_and_return_200(self, login_user, create_user):
        username = "vendor-10"
        password = "Success@2023"
        register_data = {
            "username": username,
            "password": make_password(password),
            "account_type": "V",
        }
        create_user(register_data)

        response = login_user({"username": username, "password": password})
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response_data
        assert "refresh" in response_data

    def test_if_parchaser_login_success_and_return_200(self, login_user, create_user):
        username = "parchaser-10"
        password = "Success@2023"
        register_data = {
            "username": username,
            "password": make_password(password),
            "account_type": "V",
        }
        create_user(register_data)

        response = login_user({"username": username, "password": password})
        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response_data
        assert "refresh" in response_data


# class TestTokenRenewal:
#     def test_if_refresh_token_given_and_return_200(self):
#         pass

#     def test_if_access_token_given_and_return_401(self):
#         pass

#     def test_if_invalid_refresh_token_given_and_return_401(self):
#         pass
