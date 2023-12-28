from .common import *
import dj_database_url


SECRET_KEY = 'django-insecure-+%a9#ksz)lluq!gr$@4(b6b_t-j#cd4%&nuzoz+rrqs^ds@47j'

DEBUG = True

DATABASES = {
    'default': dj_database_url.config(
        default="mysql://root:Success.2023@127.0.0.1:3306/vendorflow")
}

OPENAPI_DOCUMENT_VISIBILITY = True


INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]

INTERNAL_IPS = [
    "127.0.0.1",
]
