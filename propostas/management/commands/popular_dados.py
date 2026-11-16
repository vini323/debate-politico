"""
Carrega os candidatos do 2º turno de 2026 e um resumo das propostas
registradas nos planos de governo entregues ao TSE.

Uso:  python manage.py popular_dados
"""
from django.core.management.base import BaseCommand

from propostas.models import Candidato, Proposta, Tema

TSE = (
    "https://www.tse.jus.br/eleicoes/eleicoes-2026-content/"
    "propostas-de-governo-dos-candidatos-ao-cargo-de-presidente-da-republica-eleicoes-2026-segundo-turno"
)
FONTE_LULA = "https://www.congressoemfoco.com.br/noticia/123519/o-que-lula-promete-fazer-se-for-reeleito-presidente"
FONTE_FLAVIO = "https://www.congressoemfoco.com.br/noticia/123522/o-que-flavio-bolsonaro-promete-fazer-se-for-eleito-presidente"

# (nome, ícone, descrição)
TEMAS = [
    ("Economia", "💰", "Impostos, contas públicas, indústria e comércio"),
    ("Saúde", "🏥", "SUS, atendimento e medicamentos"),
    ("Educação", "📚", "Escolas, alfabetização e ensino superior"),
    ("Segurança pública", "🛡️", "Crime organizado, polícia e sistema prisional"),
    ("Trabalho e Previdência", "👷", "Emprego, direitos trabalhistas e INSS"),
    ("Assistência social", "🤝", "Benefícios sociais e cuidado"),
    ("Infraestrutura e energia", "🏗️", "Obras, transporte, energia"),
    ("Meio ambiente", "🌳", "Desmatamento, clima e bioeconomia"),
    ("Estado e instituições", "🏛️", "Gestão pública, Judiciário e regras eleitorais"),
]

CANDIDATOS = {
    "lula": {
        "nome": "Luiz Inácio Lula da Silva",
        "nome_urna": "Lula",
        "numero": 13,
        "partido": "PT",
        "coligacao": "Brasil Pronto pra Mais (PT, PCdoB, PV, PSB, PDT, PSOL e Rede)",
        "vice": "Geraldo Alckmin",
        "titulo_plano": "Diretrizes para o Programa de Transformação do Brasil",
        "resumo": "Plano de 84 páginas dividido em 13 diretrizes por área de governo. "
                  "Combina a continuidade de programas do mandato atual com novas metas.",
        "link_plano": TSE,
        "cor": "#c8102e",
    },
    "flavio": {
        "nome": "Flávio Nantes Bolsonaro",
        "nome_urna": "Flávio Bolsonaro",
        "numero": 22,
        "partido": "PL",
        "coligacao": "Partido Liberal (sem coligação)",
        "vice": "Alfredo Gaspar",
        "titulo_plano": "Para o Brasil Vencer o Atraso",
        "resumo": "Plano de 76 páginas dividido em nove eixos, organizado como a jornada "
                  "de um cidadão e aberto pelo tema da segurança pública.",
        "link_plano": TSE,
        "cor": "#1d4fa3",
    },
}

# (candidato, tema, título, descrição, depende do Congresso?)
PROPOSTAS = [
    # ---------------- LULA ----------------
    ("lula", "Economia", "Manter o arcabouço fiscal",
     "Seguir com a regra fiscal atual para controlar o crescimento dos gastos.", False),
    ("lula", "Economia", "Implantar a reforma tributária e o cashback",
     "Concluir as etapas da reforma dos impostos sobre consumo e devolver parte dos "
     "impostos às famílias de baixa renda (cashback).", False),
    ("lula", "Economia", "Rever benefícios fiscais e ampliar a Nova Indústria Brasil",
     "Revisar isenções consideradas ineficientes e ampliar a política industrial com "
     "financiamento, inovação e compras do governo.", True),
    ("lula", "Saúde", "Ampliar o Agora Tem Especialistas",
     "Expandir o programa para reduzir a espera por consultas e exames com especialistas.", False),
    ("lula", "Saúde", "Mais equipes de Saúde da Família e atendimento domiciliar",
     "Aumentar as equipes de atenção básica e o cuidado em casa.", False),
    ("lula", "Saúde", "Produção nacional de remédios e vacinas",
     "Ampliar a fabricação no Brasil de medicamentos e vacinas.", False),
    ("lula", "Educação", "Expandir o ensino integral",
     "Aumentar o número de escolas em tempo integral.", False),
    ("lula", "Educação", "Fortalecer o Pé-de-Meia",
     "Manter e reforçar a poupança paga a estudantes do ensino médio para evitar a evasão.", False),
    ("lula", "Educação", "Novas universidades e campus do ITA",
     "Concluir a Universidade Indígena, a Universidade do Esporte e a unidade do ITA no Ceará.", False),
    ("lula", "Segurança pública", "Criar o Ministério da Segurança Pública",
     "Criar um ministério próprio para a área, após a aprovação da PEC da Segurança.", True),
    ("lula", "Segurança pública", "Asfixia financeira das facções",
     "Intensificar investigações financeiras contra o crime organizado e integrar as polícias.", False),
    ("lula", "Segurança pública", "Câmeras corporais e presídios federais",
     "Ampliar o uso de câmeras nos uniformes policiais e fortalecer o sistema prisional federal.", False),
    ("lula", "Trabalho e Previdência", "Direitos para trabalhadores de aplicativo",
     "Regulamentar remuneração e proteção previdenciária de motoristas e entregadores.", True),
    ("lula", "Trabalho e Previdência", "Valorização do salário mínimo",
     "Manter a política de aumento real do salário mínimo e combater a 'pejotização' fraudulenta.", False),
    ("lula", "Trabalho e Previdência", "Modernizar o INSS",
     "Modernizar o atendimento e flexibilizar contribuições para quem tem carreira intermitente. "
     "Não propõe mudar a idade mínima de aposentadoria.", False),
    ("lula", "Assistência social", "Política Nacional de Cuidados",
     "Ampliar espaços para crianças, restaurantes populares, cozinhas solidárias e formação de cuidadores.", False),
    ("lula", "Assistência social", "Casas da Mulher Brasileira",
     "Concluir as unidades de atendimento a mulheres em situação de violência.", False),
    ("lula", "Infraestrutura e energia", "Nova etapa do PAC",
     "Lançar nova fase do programa de obras, com concessões e investimento privado em "
     "transporte, energia e saneamento.", False),
    ("lula", "Infraestrutura e energia", "Renováveis, biocombustíveis e petróleo",
     "Expandir energia renovável, biocombustíveis e armazenamento, mantendo investimentos "
     "em petróleo, gás e fertilizantes.", False),
    ("lula", "Meio ambiente", "Combate ao desmatamento",
     "Reforçar a fiscalização contra o desmatamento e ampliar a restauração florestal e o financiamento climático.", False),
    ("lula", "Estado e instituições", "Serviços públicos digitais",
     "Digitalizar serviços e melhorar o Gov.br, integrando a gestão entre ministérios.", False),
    ("lula", "Estado e instituições", "Rever emendas parlamentares e regras eleitorais",
     "Abrir discussão sobre mudanças no sistema de emendas e nas regras eleitorais, e ampliar a participação social.", True),

    # ---------------- FLÁVIO BOLSONARO ----------------
    ("flavio", "Economia", "Rever a reforma tributária",
     "Revisar a reforma para reduzir a alíquota prevista do novo imposto sobre consumo (IVA).", True),
    ("flavio", "Economia", "Novas regras fiscais e superávit",
     "Reescrever as regras fiscais, buscar superávit primário e reduzir a dívida em relação ao PIB.", True),
    ("flavio", "Economia", "Privatizações e abertura comercial",
     "Retomar privatizações, limitar crédito subsidiado do Tesouro e retomar a entrada do Brasil na OCDE.", False),
    ("flavio", "Saúde", "Prontuário eletrônico único",
     "Criar um registro de saúde único para cada paciente em todo o país.", False),
    ("flavio", "Saúde", "Telessaúde e agendamento com IA",
     "Ampliar o atendimento a distância e usar inteligência artificial para marcar consultas.", False),
    ("flavio", "Saúde", "Usar vagas da rede privada",
     "Aproveitar horários disponíveis em clínicas e hospitais privados para reduzir filas do SUS.", False),
    ("flavio", "Educação", "Alfabetização pelo método fônico",
     "Adotar o método fônico como base da alfabetização.", False),
    ("flavio", "Educação", "Escolas cívico-militares",
     "Criar escolas no modelo cívico-militar.", False),
    ("flavio", "Educação", "Vouchers e financiamento por resultado",
     "Oferecer vagas pagas em escolas e creches privadas quando faltar vaga pública, "
     "e ligar o repasse de recursos aos resultados das escolas.", True),
    ("flavio", "Segurança pública", "Reduzir a maioridade penal para 16 anos",
     "Baixar a maioridade penal de 18 para 16 anos e punir adolescentes a partir de 14 anos por crimes graves.", True),
    ("flavio", "Segurança pública", "Facções como organizações narcoterroristas",
     "Classificar PCC e Comando Vermelho como organizações narcoterroristas.", True),
    ("flavio", "Segurança pública", "Penas mais duras e mais presídios",
     "Acabar com a progressão de regime para crimes hediondos, aprovar castração química para "
     "estupradores e abusadores de crianças e ampliar o sistema prisional.", True),
    ("flavio", "Trabalho e Previdência", "Negociado sobre o legislado",
     "Reduzir custos de contratação e fazer acordos entre patrão e empregado prevalecerem sobre a lei.", True),
    ("flavio", "Trabalho e Previdência", "Emprego para jovens e pessoas 50+",
     "Criar formas de contratação para quem tem de 18 a 24 anos e incentivos para contratar maiores de 50.", True),
    ("flavio", "Trabalho e Previdência", "INSS sem fila",
     "Modernizar o INSS, reduzir filas e combater fraudes. Não detalha mudanças na idade mínima.", False),
    ("flavio", "Assistência social", "Benefícios ligados a emprego e crédito",
     "Manter os benefícios sociais e integrá-los a políticas de emprego e crédito.", False),
    ("flavio", "Assistência social", "Atendimento a mulheres, idosos e pessoas com deficiência",
     "Criar serviços específicos para esses públicos.", False),
    ("flavio", "Infraestrutura e energia", "Investimento privado e corredores logísticos",
     "Ampliar o investimento privado, modernizar marcos regulatórios e desenvolver corredores logísticos.", True),
    ("flavio", "Infraestrutura e energia", "Gás, refino e conta de luz mais barata",
     "Expandir a infraestrutura de gás natural, modernizar o refino, incentivar biocombustíveis "
     "e reduzir encargos na conta de luz mantendo a tarifa social.", False),
    ("flavio", "Meio ambiente", "Licenciamento ambiental mais simples",
     "Simplificar o licenciamento e ampliar pagamentos por serviços ambientais.", True),
    ("flavio", "Meio ambiente", "Bioeconomia e minerais críticos",
     "Incentivar a bioeconomia e a exploração de minerais críticos.", False),
    ("flavio", "Estado e instituições", "Enxugar a máquina pública",
     "Cortar cargos comissionados e gastos administrativos, combater supersalários e usar critérios "
     "técnicos para dirigir estatais e agências reguladoras.", False),
    ("flavio", "Estado e instituições", "Mudanças no STF",
     "Retirar do STF o julgamento de processos criminais, limitar decisões individuais de ministros "
     "e exigir quarentena para ex-ministros de Estado serem indicados à Corte.", True),
    ("flavio", "Estado e instituições", "Fim da reeleição para presidente",
     "Acabar com a reeleição presidencial, o que exige emenda à Constituição.", True),
]


class Command(BaseCommand):
    help = "Carrega candidatos, temas e propostas dos planos de governo de 2026."

    def handle(self, *args, **options):
        temas = {}
        for ordem, (nome, icone, desc) in enumerate(TEMAS, start=1):
            temas[nome], _ = Tema.objects.update_or_create(
                nome=nome, defaults={"icone": icone, "descricao": desc, "ordem": ordem}
            )

        candidatos = {}
        for chave, dados in CANDIDATOS.items():
            candidatos[chave], _ = Candidato.objects.update_or_create(
                numero=dados["numero"], defaults=dados
            )

        fontes = {"lula": FONTE_LULA, "flavio": FONTE_FLAVIO}
        criadas = 0
        for chave, tema, titulo, descricao, congresso in PROPOSTAS:
            _, criada = Proposta.objects.update_or_create(
                candidato=candidatos[chave], titulo=titulo,
                defaults={
                    "tema": temas[tema], "descricao": descricao,
                    "depende_congresso": congresso, "fonte": fontes[chave],
                },
            )
            criadas += criada

        self.stdout.write(self.style.SUCCESS(
            f"{len(temas)} temas, {len(candidatos)} candidatos e {len(PROPOSTAS)} propostas "
            f"carregados ({criadas} novas)."
        ))
