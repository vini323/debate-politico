from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil


class CadastroForm(UserCreationForm):
    """Cadastro simples: nome de usuário, e-mail e senha."""

    email = forms.EmailField(label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        labels = {"username": "Nome de usuário"}

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email


class DadosUsuarioForm(forms.ModelForm):
    """Edita nome e e-mail do usuário logado."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Nome", "last_name": "Sobrenome", "email": "E-mail"}

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Já existe outra conta com este e-mail.")
        return email


class PerfilForm(forms.ModelForm):
    """Dados pessoais extras (model Perfil)."""

    class Meta:
        model = Perfil
        fields = ("telefone", "data_nascimento", "cidade", "estado")
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000"}),
        }
