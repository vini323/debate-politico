from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Debate Político — Administração"
admin.site.site_title = "Debate Político"
admin.site.index_title = "Painel de administração"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("debate.urls")),
]
