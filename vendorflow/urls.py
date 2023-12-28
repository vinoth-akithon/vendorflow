from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("vms.urls")),
]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

if settings.OPENAPI_DOCUMENT_VISIBILITY:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    urlpatterns += [
        path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
        path("docs/swagger/",
             SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
        path("docs/redoc/",
             SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]
