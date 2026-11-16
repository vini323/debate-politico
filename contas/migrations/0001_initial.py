import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telefone", models.CharField(blank=True, max_length=20, verbose_name="telefone")),
                ("data_nascimento", models.DateField(blank=True, null=True, verbose_name="data de nascimento")),
                ("cidade", models.CharField(blank=True, max_length=80, verbose_name="cidade")),
                ("estado", models.CharField(blank=True, choices=[("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"), ("BA", "Bahia"), ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espírito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"), ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"), ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"), ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"), ("SC", "Santa Catarina"), ("SP", "São Paulo"), ("SE", "Sergipe"), ("TO", "Tocantins")], max_length=2, verbose_name="estado")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="cadastrado em")),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="perfil", to=settings.AUTH_USER_MODEL, verbose_name="usuário")),
            ],
            options={
                "verbose_name": "perfil",
                "verbose_name_plural": "perfis",
            },
        ),
    ]
