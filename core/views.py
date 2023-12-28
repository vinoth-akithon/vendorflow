from django.shortcuts import render
from django.db.transaction import atomic
from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import User
from .serializers import UserCreateSerializer
from vms.models import Purchaser, Vendor
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

# working code
# class UserCreateView(APIView):
#     def post(self, request: Request) -> Response:
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data

#         profile_details = {
#             "name": validated_data.pop("name", ""),
#             "contact_details": validated_data.pop("contact_details", ""),
#             "address": validated_data.pop("address", "")
#         }

#         # password hashing
#         validated_data["password"] = make_password(validated_data["password"])
#         user = serializer.save()

#         if validated_data["account_type"] == "V":
#             Vendor.objects.create(
#                 user_id=user.id, **profile_details)
#         elif validated_data["account_type"] == "P":
#             Purchaser.objects.create(
#                 user_id=user.id, **profile_details)

#         validated_data.pop("password", None)
#         return Response({**profile_details, **validated_data}, status=HTTP_201_CREATED)


@extend_schema(description="Takes user basic details and login credentials \
    and perform Registration based on account type.\
    Account Type should be either `P` for Purchaser and `V` for Vendor.\
    *Allowed Users*: [`AnyOne`]",
               summary="Register new user")
class UserRegisterView(CreateAPIView):
    """
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request: Request) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        profile_details = {
            "name": validated_data.pop("name", ""),
            "contact_details": validated_data.pop("contact_details", ""),
            "address": validated_data.pop("address", "")
        }

        # password hashing
        validated_data["password"] = make_password(validated_data["password"])
        user = serializer.save()

        if validated_data["account_type"] == "V":
            Vendor.objects.create(
                user_id=user.id, **profile_details)
        elif validated_data["account_type"] == "P":
            Purchaser.objects.create(
                user_id=user.id, **profile_details)

        validated_data.pop("password", None)
        return Response({**profile_details, **validated_data}, status=HTTP_201_CREATED)


@extend_schema(summary="Login uset and get JWT tokens")
class UserLoginView(TokenObtainPairView):
    """ Takes user credentials and perform Authendication.
    Returns `access` and `refresh` tokens for Authorization.
    *Allowed Users*: [`Admin`, `Vendor`, `Purchaser`]
    """


@extend_schema(summary="Renew token")
class UserTokenRefreshView(TokenRefreshView):
    """ Takes valid `refresh` token.
    Returns new `access` token for further Authorization.
    *Allowed Users*: [`Admin`, `Vendor`, `Purchaser`]
    """
