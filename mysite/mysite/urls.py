
from django.contrib import admin
from django.urls import include, path
from django.contrib.admin.views.decorators import staff_member_required

admin.site.login = staff_member_required(admin.site.login, login_url='/login/')

urlpatterns = [
    path("", include('sitex.urls')),
    path("admin/", admin.site.urls),
]
