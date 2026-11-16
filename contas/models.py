from django.conf import settings
from django.db import models

ESTADOS = [
    ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"),
    ("BA", "Bahia"), ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espírito Santo"),
    ("GO", "Goiás"), ("MA", "Maranhão"), ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"),
    ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"), ("SC", "Santa Catarina"),
    ("SP", "São Paulo"), ("SE", "Sergipe"), ("TO", "Tocantins"),
]


class Perfil(models.Model):
    """Dados extras do usuário, ligados 1 para 1 ao User do Django."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="perfil", verbose_name="usuário",
    )
    telefone = models.CharField("telefone", max_length=20, blank=True)
    data_nascimento = models.DateField("data de nascimento", null=True, blank=True)
    cidade = models.CharField("cidade", max_length=80, blank=True)
    estado = models.CharField("estado", max_length=2, choices=ESTADOS, blank=True)
    criado_em = models.DateTimeField("cadastrado em", auto_now_add=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfis"

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"
