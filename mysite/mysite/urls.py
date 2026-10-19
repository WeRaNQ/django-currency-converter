
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", include('sitex.urls')),
    path("admin/", admin.site.urls),
    path("logout",LogoutView.as_view(next_page = "/"), name = "logout"),
]
