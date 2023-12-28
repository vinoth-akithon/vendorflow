from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    VENDOR = "V"
    PARCHASER = "P"
    ACCOUNT_TYPE = [
        (PARCHASER, "Parchaser"),
        (VENDOR, "Vendor"),
    ]
    account_type = models.CharField(
        max_length=1, choices=ACCOUNT_TYPE, default="")
