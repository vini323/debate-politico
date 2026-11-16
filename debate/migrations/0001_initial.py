import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Politico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120, verbose_name="nome")),
                ("partido", models.CharField(max_length=60, verbose_name="partido")),
                ("cargo", models.CharField(help_text="Ex.: Presidente da República", max_length=120, verbose_name="cargo")),
                ("periodo", models.CharField(blank=True, max_length=60, verbose_name="período do governo")),
                ("biografia", models.TextField(blank=True, verbose_name="biografia")),
                ("foto_url", models.URLField(blank=True, verbose_name="URL da foto")),
            ],
            options={
                "verbose_name": "político",
                "verbose_name_plural": "políticos",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Tema",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=80, unique=True, verbose_name="nome")),
                ("descricao", models.TextField(blank=True, verbose_name="descrição")),
            ],
            options={
                "verbose_name": "tema",
                "verbose_name_plural": "temas",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Argumento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("posicao", models.CharField(choices=[("D", "Defesa"), ("C", "Crítica")], max_length=1, verbose_name="posição")),
                ("titulo", models.CharField(max_length=150, verbose_name="título")),
                ("texto", models.TextField(verbose_name="argumento")),
                ("fonte", models.URLField(blank=True, help_text="Link que embasa o argumento", verbose_name="fonte (link)")),
                ("autor", models.CharField(max_length=80, verbose_name="autor")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("atualizado_em", models.DateTimeField(auto_now=True, verbose_name="atualizado em")),
                ("politico", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="argumentos", to="debate.politico", verbose_name="político")),
                ("tema", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="argumentos", to="debate.tema", verbose_name="tema")),
            ],
            options={
                "verbose_name": "argumento",
                "verbose_name_plural": "argumentos",
                "ordering": ["-criado_em"],
            },
        ),
        migrations.CreateModel(
            name="Comentario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("autor", models.CharField(max_length=80, verbose_name="autor")),
                ("texto", models.TextField(verbose_name="comentário")),
                ("concorda", models.BooleanField(default=True, verbose_name="concorda com o argumento?")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("aprovado", models.BooleanField(default=True, verbose_name="aprovado")),
                ("argumento", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comentarios", to="debate.argumento", verbose_name="argumento")),
            ],
            options={
                "verbose_name": "comentário",
                "verbose_name_plural": "comentários",
                "ordering": ["criado_em"],
            },
        ),
    ]
