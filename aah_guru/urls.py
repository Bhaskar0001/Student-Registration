from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("students:register")),
    path("django-admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("students.urls")),
    path("", include("parents.urls")),
    path("", include("dashboards.urls")),
    path("", include("audit.urls")),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
