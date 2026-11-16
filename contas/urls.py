from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "contas"

urlpatterns = [
    path("entrar/", auth_views.LoginView.as_view(
        template_name="contas/login.html", redirect_authenticated_user=True,
    ), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("meus-dados/", views.meus_dados, name="meus_dados"),
    path("meus-dados/senha/", views.TrocarSenhaView.as_view(), name="trocar_senha"),
]
