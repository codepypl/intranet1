from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('account.urls', namespace='konto')),
    path("konto/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
