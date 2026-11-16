"""Cria dados de exemplo para a apresentação: python manage.py popular_dados"""
from django.core.management.base import BaseCommand

from debate.models import Argumento, Comentario, Politico, Tema

TEMAS = [
    ("Economia", "Inflação, emprego, juros, contas públicas."),
    ("Saúde", "SUS, vacinação, filas e hospitais."),
    ("Segurança", "Violência, crime organizado, polícia."),
    ("Educação", "Escolas, universidades e alfabetização."),
    ("Meio ambiente", "Desmatamento, clima e agronegócio."),
]

POLITICOS = [
    {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "cargo": "Presidente da República",
        "periodo": "2023–2026 · reeleito para 2027–2030",
        "biografia": "Presidente do Brasil em 2003–2010 e desde 2023. Reeleito no 2º turno de 2026.",
    },
    {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "cargo": "Senador (RJ)",
        "periodo": "Senado desde 2019",
        "biografia": "Senador pelo Rio de Janeiro e candidato do PL à Presidência em 2026. "
                     "Aqui se debatem sua atuação e suas propostas de governo.",
    },
]

# (índice do político, tema, posição, título, texto)
ARGUMENTOS = [
    (0, "Economia", "D", "Programas sociais aquecem o consumo",
     "Exemplo de defesa: a ampliação de programas de transferência de renda ajuda a "
     "movimentar o comércio local e reduzir a pobreza."),
    (0, "Economia", "C", "Gastos públicos pressionam as contas",
     "Exemplo de crítica: o aumento de despesas sem cortes equivalentes pode elevar a "
     "dívida pública e manter os juros altos."),
    (1, "Segurança", "D", "Foco em segurança pública",
     "Exemplo de defesa: as propostas de endurecimento penal respondem a uma demanda "
     "real da população por mais segurança."),
    (1, "Meio ambiente", "C", "Propostas ambientais pouco claras",
     "Exemplo de crítica: faltam metas concretas de combate ao desmatamento nas "
     "propostas apresentadas."),
]


class Command(BaseCommand):
    help = "Popula o banco com temas, políticos, argumentos e comentários de exemplo."

    def handle(self, *args, **options):
        temas = {}
        for nome, desc in TEMAS:
            temas[nome], _ = Tema.objects.get_or_create(nome=nome, defaults={"descricao": desc})

        politicos = []
        for dados in POLITICOS:
            p, _ = Politico.objects.get_or_create(nome=dados["nome"], defaults=dados)
            politicos.append(p)

        for i, tema, pos, titulo, texto in ARGUMENTOS:
            arg, criado = Argumento.objects.get_or_create(
                titulo=titulo,
                defaults={
                    "politico": politicos[i], "tema": temas[tema], "posicao": pos,
                    "texto": texto, "autor": "Exemplo",
                },
            )
            if criado:
                Comentario.objects.create(
                    argumento=arg, autor="Leitor 1", concorda=True,
                    texto="Concordo, faz sentido.",
                )
                Comentario.objects.create(
                    argumento=arg, autor="Leitor 2", concorda=False,
                    texto="Discordo, faltam dados para sustentar isso.",
                )

        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados!"))
