import os
from .common import *
import dj_database_url

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS").split(" ")]

DATABASES = {
    'default': dj_database_url.config(os.getenv("DATABASE_URL"))
}

OPENAPI_DOCUMENT_VISIBILITY = os.getenv("OPENAPI_DOCUMENT_VISIBILITY", False)
