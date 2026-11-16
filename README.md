# Propostas 2026 🗳️

Trabalho final — **Desenvolvimento Web com Python e Django**.

Aplicação MTV (Model–Template–View) que apresenta as **propostas dos planos de governo** de **Lula (PT, 13)** e **Flávio Bolsonaro (PL, 22)**, candidatos do 2º turno da eleição presidencial de 2026. As propostas são organizadas por tema para comparar os dois candidatos lado a lado.

## Requisitos do trabalho

| Requisito | Onde está |
|---|---|
| Tema/abordagem | Vitrine e comparação das propostas dos candidatos à Presidência |
| Mínimo de 3 models relacionados | `Candidato`, `Tema`, `Proposta` (`propostas/models.py`) |
| Administração pelo painel Admin | `propostas/admin.py`: filtros, busca, propostas dentro do candidato |
| Template de **listar** registros | `proposta_lista.html`, `candidato_lista.html` |
| Template de **detalhes** | `proposta_detalhe.html`, `candidato_detalhe.html` |
| Template de **editar** | `proposta_form.html`, `candidato_form.html` (UpdateView) |
| Template de **criar** | `proposta_form.html`, `candidato_form.html` (CreateView) |
| Versionado no GitHub | este repositório |

### Relacionamentos

```
Candidato 1 ──── N Proposta N ──── 1 Tema
```

- `Proposta.candidato` → `ForeignKey(Candidato)`
- `Proposta.tema` → `ForeignKey(Tema)`

## Páginas

- **Início**: os dois candidatos e a grade de temas
- **Comparar por tema** (`/comparar/<id>/`): propostas dos dois candidatos em colunas
- **Propostas**: lista com busca, filtro por candidato/tema e paginação; detalhe, criar, editar e excluir
- **Candidatos**: lista, ficha do candidato com propostas agrupadas por tema, criar, editar e excluir
- **Admin**: `/admin/`

## Como rodar (Windows)

Dê dois cliques em **`rodar_site.bat`**. Ele cria o ambiente virtual, instala o Django, cria o banco, carrega as propostas e abre o site.

Ou manualmente:

```bash
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py popular_dados  # carrega candidatos, temas e propostas
python manage.py createsuperuser
python manage.py runserver
```

## Fontes dos dados

Resumo próprio das propostas, com base nos planos registrados no TSE:

- TSE — Propostas de governo, 2º turno 2026: https://www.tse.jus.br/eleicoes/eleicoes-2026-content/propostas-de-governo-dos-candidatos-ao-cargo-de-presidente-da-republica-eleicoes-2026-segundo-turno
- Congresso em Foco — O que Lula promete: https://www.congressoemfoco.com.br/noticia/123519/o-que-lula-promete-fazer-se-for-reeleito-presidente
- Congresso em Foco — O que Flávio Bolsonaro promete: https://www.congressoemfoco.com.br/noticia/123522/o-que-flavio-bolsonaro-promete-fazer-se-for-eleito-presidente
