from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Perfil


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = "dados pessoais"


# Mostra os dados do perfil dentro da tela de usuário do admin
admin.site.unregister(User)


@admin.register(User)
class UsuarioAdmin(UserAdmin):
    inlines = [PerfilInline]
    list_display = ("username", "email", "first_name", "last_name", "cidade", "is_staff")

    @admin.display(description="cidade")
    def cidade(self, obj):
        perfil = getattr(obj, "perfil", None)
        if perfil and perfil.cidade:
            return f"{perfil.cidade}/{perfil.estado}" if perfil.estado else perfil.cidade
        return "—"


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cidade", "estado", "telefone", "criado_em")
    list_filter = ("estado",)
    search_fields = ("usuario__username", "usuario__email", "cidade")
