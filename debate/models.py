from django.db import models
from django.urls import reverse


class Politico(models.Model):
    """Figura política cujo governo está em debate (ex.: Lula, Flávio Bolsonaro)."""

    nome = models.CharField("nome", max_length=120)
    partido = models.CharField("partido", max_length=60)
    cargo = models.CharField("cargo", max_length=120, help_text="Ex.: Presidente da República")
    periodo = models.CharField("período do governo", max_length=60, blank=True)
    biografia = models.TextField("biografia", blank=True)
    foto_url = models.URLField("URL da foto", blank=True)

    class Meta:
        verbose_name = "político"
        verbose_name_plural = "políticos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.partido})"

    def get_absolute_url(self):
        return reverse("debate:politico_detalhe", args=[self.pk])

    @property
    def total_defesas(self):
        return self.argumentos.filter(posicao=Argumento.DEFESA).count()

    @property
    def total_criticas(self):
        return self.argumentos.filter(posicao=Argumento.CRITICA).count()


class Tema(models.Model):
    """Área de governo em discussão (economia, saúde, segurança...)."""

    nome = models.CharField("nome", max_length=80, unique=True)
    descricao = models.TextField("descrição", blank=True)

    class Meta:
        verbose_name = "tema"
        verbose_name_plural = "temas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Argumento(models.Model):
    """Uma defesa ou crítica ao governo de um político, sobre um tema."""

    DEFESA = "D"
    CRITICA = "C"
    POSICOES = [
        (DEFESA, "Defesa"),
        (CRITICA, "Crítica"),
    ]

    politico = models.ForeignKey(
        Politico, on_delete=models.CASCADE, related_name="argumentos", verbose_name="político"
    )
    tema = models.ForeignKey(
        Tema, on_delete=models.PROTECT, related_name="argumentos", verbose_name="tema"
    )
    posicao = models.CharField("posição", max_length=1, choices=POSICOES)
    titulo = models.CharField("título", max_length=150)
    texto = models.TextField("argumento")
    fonte = models.URLField("fonte (link)", blank=True, help_text="Link que embasa o argumento")
    autor = models.CharField("autor", max_length=80)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "argumento"
        verbose_name_plural = "argumentos"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"[{self.get_posicao_display()}] {self.titulo}"

    def get_absolute_url(self):
        return reverse("debate:argumento_detalhe", args=[self.pk])


class Comentario(models.Model):
    """Comentário de um leitor sobre um argumento."""

    argumento = models.ForeignKey(
        Argumento, on_delete=models.CASCADE, related_name="comentarios", verbose_name="argumento"
    )
    autor = models.CharField("autor", max_length=80)
    texto = models.TextField("comentário")
    concorda = models.BooleanField("concorda com o argumento?", default=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    aprovado = models.BooleanField("aprovado", default=True)

    class Meta:
        verbose_name = "comentário"
        verbose_name_plural = "comentários"
        ordering = ["criado_em"]

    def __str__(self):
        return f"{self.autor} em “{self.argumento.titulo}”"
