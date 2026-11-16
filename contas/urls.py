from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

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

    # Esqueci minha senha (envia link por e-mail)
    path("senha/esqueci/", auth_views.PasswordResetView.as_view(
        template_name="contas/esqueci_senha.html",
        email_template_name="contas/email_redefinir_senha.txt",
        subject_template_name="contas/email_redefinir_assunto.txt",
        success_url=reverse_lazy("contas:senha_enviada"),
    ), name="esqueci_senha"),
    path("senha/enviada/", auth_views.PasswordResetDoneView.as_view(
        template_name="contas/senha_enviada.html",
    ), name="senha_enviada"),
    path("senha/redefinir/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="contas/redefinir_senha.html",
        success_url=reverse_lazy("contas:senha_redefinida"),
    ), name="redefinir_senha"),
    path("senha/redefinida/", auth_views.PasswordResetCompleteView.as_view(
        template_name="contas/senha_redefinida.html",
    ), name="senha_redefinida"),
]
