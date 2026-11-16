import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candidato",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120, verbose_name="nome")),
                ("nome_urna", models.CharField(max_length=60, verbose_name="nome na urna")),
                ("numero", models.PositiveSmallIntegerField(verbose_name="número na urna")),
                ("partido", models.CharField(max_length=20, verbose_name="partido")),
                ("coligacao", models.CharField(blank=True, max_length=200, verbose_name="coligação")),
                ("vice", models.CharField(blank=True, max_length=120, verbose_name="candidato a vice")),
                ("titulo_plano", models.CharField(blank=True, max_length=200, verbose_name="título do plano de governo")),
                ("resumo", models.TextField(blank=True, verbose_name="resumo do plano")),
                ("link_plano", models.URLField(blank=True, verbose_name="link do plano no TSE")),
                ("cor", models.CharField(default="#1f3a5f", help_text="Cor em hexadecimal usada nos cartões (ex.: #c8102e)", max_length=7, verbose_name="cor de destaque")),
            ],
            options={
                "verbose_name": "candidato",
                "verbose_name_plural": "candidatos",
                "ordering": ["nome_urna"],
            },
        ),
        migrations.CreateModel(
            name="Tema",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=80, unique=True, verbose_name="nome")),
                ("icone", models.CharField(blank=True, max_length=8, verbose_name="ícone (emoji)")),
                ("descricao", models.CharField(blank=True, max_length=200, verbose_name="descrição")),
                ("ordem", models.PositiveSmallIntegerField(default=0, verbose_name="ordem de exibição")),
            ],
            options={
                "verbose_name": "tema",
                "verbose_name_plural": "temas",
                "ordering": ["ordem", "nome"],
            },
        ),
        migrations.CreateModel(
            name="Proposta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=160, verbose_name="título")),
                ("descricao", models.TextField(verbose_name="descrição")),
                ("depende_congresso", models.BooleanField(default=False, help_text="Marque se a proposta precisa de lei ou emenda constitucional", verbose_name="depende do Congresso?")),
                ("fonte", models.URLField(blank=True, verbose_name="fonte (link)")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("atualizado_em", models.DateTimeField(auto_now=True, verbose_name="atualizado em")),
                ("candidato", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="propostas", to="propostas.candidato", verbose_name="candidato")),
                ("tema", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="propostas", to="propostas.tema", verbose_name="tema")),
            ],
            options={
                "verbose_name": "proposta",
                "verbose_name_plural": "propostas",
                "ordering": ["tema__ordem", "candidato__nome_urna", "titulo"],
            },
        ),
    ]
