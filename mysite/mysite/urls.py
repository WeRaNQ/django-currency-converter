
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("index/", include("sitex.urls")),
    path('admin/', admin.site.urls),
]
