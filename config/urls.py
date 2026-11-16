from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Propostas 2026 — Administração"
admin.site.site_title = "Propostas 2026"
admin.site.index_title = "Painel de administração"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contas/", include("contas.urls")),
    path("", include("propostas.urls")),
]
