from django.db import models
from django.urls import reverse


class Candidato(models.Model):
    """Candidato à Presidência e seu plano de governo."""

    nome = models.CharField("nome", max_length=120)
    nome_urna = models.CharField("nome na urna", max_length=60)
    numero = models.PositiveSmallIntegerField("número na urna")
    partido = models.CharField("partido", max_length=20)
    coligacao = models.CharField("coligação", max_length=200, blank=True)
    vice = models.CharField("candidato a vice", max_length=120, blank=True)
    titulo_plano = models.CharField("título do plano de governo", max_length=200, blank=True)
    resumo = models.TextField("resumo do plano", blank=True)
    link_plano = models.URLField("link do plano no TSE", blank=True)
    cor = models.CharField(
        "cor de destaque", max_length=7, default="#1f3a5f",
        help_text="Cor em hexadecimal usada nos cartões (ex.: #c8102e)",
    )

    class Meta:
        verbose_name = "candidato"
        verbose_name_plural = "candidatos"
        ordering = ["nome_urna"]

    def __str__(self):
        return f"{self.nome_urna} ({self.partido} {self.numero})"

    def get_absolute_url(self):
        return reverse("propostas:candidato_detalhe", args=[self.pk])


class Tema(models.Model):
    """Área de governo usada para comparar as propostas (Economia, Saúde...)."""

    nome = models.CharField("nome", max_length=80, unique=True)
    icone = models.CharField("ícone (emoji)", max_length=8, blank=True)
    descricao = models.CharField("descrição", max_length=200, blank=True)
    ordem = models.PositiveSmallIntegerField("ordem de exibição", default=0)

    class Meta:
        verbose_name = "tema"
        verbose_name_plural = "temas"
        ordering = ["ordem", "nome"]

    def __str__(self):
        return f"{self.icone} {self.nome}".strip()

    def get_absolute_url(self):
        return reverse("propostas:tema_comparar", args=[self.pk])


class Proposta(models.Model):
    """Uma proposta do plano de governo de um candidato, dentro de um tema."""

    candidato = models.ForeignKey(
        Candidato, on_delete=models.CASCADE, related_name="propostas", verbose_name="candidato"
    )
    tema = models.ForeignKey(
        Tema, on_delete=models.PROTECT, related_name="propostas", verbose_name="tema"
    )
    titulo = models.CharField("título", max_length=160)
    descricao = models.TextField("descrição")
    depende_congresso = models.BooleanField(
        "depende do Congresso?", default=False,
        help_text="Marque se a proposta precisa de lei ou emenda constitucional",
    )
    fonte = models.URLField("fonte (link)", blank=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "proposta"
        verbose_name_plural = "propostas"
        ordering = ["tema__ordem", "candidato__nome_urna", "titulo"]

    def __str__(self):
        return f"{self.candidato.nome_urna}: {self.titulo}"

    def get_absolute_url(self):
        return reverse("propostas:proposta_detalhe", args=[self.pk])
