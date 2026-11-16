# Debate Político 🇧🇷

Trabalho final — **Desenvolvimento Web com Python e Django**.

Aplicação MTV (Model–Template–View) onde usuários publicam **defesas** e **críticas** aos governos/atuação de **Lula** e **Flávio Bolsonaro**, organizadas por tema, e comentam os argumentos uns dos outros.

## Requisitos do trabalho

| Requisito | Onde está |
|---|---|
| Tema/abordagem | Debate político: defesas e críticas a Lula e Flávio Bolsonaro |
| Mínimo de 3 models relacionados | `Politico`, `Tema`, `Argumento`, `Comentario` (`debate/models.py`) |
| Administração pelo painel Admin | `debate/admin.py` — filtros, busca, inlines e ações de moderação |
| Template de **listar** registros | `argumento_lista.html`, `politico_lista.html` |
| Template de **detalhes** | `argumento_detalhe.html`, `politico_detalhe.html` |
| Template de **editar** | `argumento_form.html`, `politico_form.html` (UpdateView) |
| Template de **criar** | `argumento_form.html`, `politico_form.html` (CreateView) |
| Versionado no GitHub | este repositório |

### Relacionamentos

```
Politico 1 ──── N Argumento N ──── 1 Tema
                     │
                     1
                     │
                     N
                 Comentario
```

- `Argumento.politico` → `ForeignKey(Politico)`
- `Argumento.tema` → `ForeignKey(Tema)`
- `Comentario.argumento` → `ForeignKey(Argumento)`
- `Argumento.posicao` → **Defesa** ou **Crítica**

## Como rodar

```bash
python -m venv venv
# Windows: venv\Scripts\activate    |   Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py popular_dados        # dados de exemplo (opcional)
python manage.py createsuperuser      # usuário do painel Admin
python manage.py runserver
```

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Funcionalidades

- Página inicial com placar de defesas × críticas de cada político
- Lista de argumentos com busca, filtros (político, posição, tema) e paginação
- Detalhe do argumento com comentários ("concordo" / "discordo")
- Criar, editar e excluir argumentos e políticos
- Admin com moderação de comentários (aprovar/ocultar)

## Atalhos para Windows

- `rodar_site.bat` — cria o ambiente virtual, instala o Django, cria o banco com exemplos e abre o servidor.
- `enviar_github.bat` — envia o projeto para um repositório do GitHub (crie o repositório vazio antes em https://github.com/new).
