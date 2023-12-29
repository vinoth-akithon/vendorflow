from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    VENDOR = "V"
    PURCHASER = "P"
    ACCOUNT_TYPE = [
        (PURCHASER, "Purchaser"),
        (VENDOR, "Vendor"),
    ]
    account_type = models.CharField(
        max_length=1, choices=ACCOUNT_TYPE, default="")
