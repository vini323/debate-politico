from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CadastroForm, DadosUsuarioForm, PerfilForm
from .models import Perfil


def cadastro(request):
    """Cria a conta (usuário, e-mail e senha) e já deixa a pessoa logada."""
    if request.user.is_authenticated:
        return redirect("propostas:inicio")

    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()
                Perfil.objects.create(usuario=usuario)
            login(request, usuario)
            messages.success(request, f"Bem-vindo(a), {usuario.username}! Sua conta foi criada.")
            return redirect("propostas:inicio")
    else:
        form = CadastroForm()

    return render(request, "contas/cadastro.html", {"form": form})


@login_required
def meus_dados(request):
    """Mostra e edita os dados do usuário logado."""
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form = DadosUsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid() and perfil_form.is_valid():
            form.save()
            perfil_form.save()
            messages.success(request, "Seus dados foram atualizados.")
            return redirect("contas:meus_dados")
    else:
        form = DadosUsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, "contas/meus_dados.html", {
        "form": form, "perfil_form": perfil_form, "perfil": perfil,
    })


class TrocarSenhaView(SuccessMessageMixin, PasswordChangeView):
    template_name = "contas/trocar_senha.html"
    success_url = reverse_lazy("contas:meus_dados")
    success_message = "Senha alterada com sucesso."
