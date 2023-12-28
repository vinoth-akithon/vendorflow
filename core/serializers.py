from rest_framework import serializers
from .models import User

# working code
# class UserCreateSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=50)
#     contact_details = serializers.CharField(allow_blank=True)
#     address = serializers.CharField(allow_blank=True)

#     class Meta:
#         model = User
#         fields = ["username", "password", "account_type",
#                   "name", "contact_details", "address"]


class UserCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    contact_details = serializers.CharField(
        allow_blank=True, style={'base_template': 'textarea.html'})
    address = serializers.CharField(allow_blank=True, style={
                                    'base_template': 'textarea.html'})

    class Meta:
        model = User
        fields = ["username", "password", "name", "account_type",
                  "contact_details", "address"]
