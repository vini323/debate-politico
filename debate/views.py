from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ArgumentoForm, ComentarioForm, PoliticoForm
from .models import Argumento, Politico, Tema


# ---------- Página inicial ----------

class InicioView(ListView):
    """Lado a lado: os políticos em debate e os argumentos mais recentes."""

    template_name = "debate/inicio.html"
    context_object_name = "politicos"

    def get_queryset(self):
        return Politico.objects.annotate(
            n_defesas=Count("argumentos", filter=Q(argumentos__posicao=Argumento.DEFESA)),
            n_criticas=Count("argumentos", filter=Q(argumentos__posicao=Argumento.CRITICA)),
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recentes"] = Argumento.objects.select_related("politico", "tema")[:6]
        return ctx


# ---------- Argumentos (CRUD completo) ----------

class ArgumentoListView(ListView):
    model = Argumento
    template_name = "debate/argumento_lista.html"
    context_object_name = "argumentos"
    paginate_by = 10

    def get_queryset(self):
        qs = Argumento.objects.select_related("politico", "tema").annotate(
            n_comentarios=Count("comentarios", filter=Q(comentarios__aprovado=True))
        )
        politico = self.request.GET.get("politico")
        posicao = self.request.GET.get("posicao")
        tema = self.request.GET.get("tema")
        busca = self.request.GET.get("q")
        if politico:
            qs = qs.filter(politico_id=politico)
        if posicao in (Argumento.DEFESA, Argumento.CRITICA):
            qs = qs.filter(posicao=posicao)
        if tema:
            qs = qs.filter(tema_id=tema)
        if busca:
            qs = qs.filter(Q(titulo__icontains=busca) | Q(texto__icontains=busca))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["politicos"] = Politico.objects.all()
        ctx["temas"] = Tema.objects.all()
        ctx["filtros"] = self.request.GET
        # mantém os filtros na paginação
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()
        return ctx


class ArgumentoDetailView(DetailView):
    model = Argumento
    template_name = "debate/argumento_detalhe.html"
    context_object_name = "argumento"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comentarios"] = self.object.comentarios.filter(aprovado=True)
        ctx["form"] = kwargs.get("form") or ComentarioForm()
        return ctx

    def post(self, request, *args, **kwargs):
        """Recebe um novo comentário para este argumento."""
        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.argumento = self.object
            comentario.save()
            messages.success(request, "Comentário publicado!")
            return redirect(self.object.get_absolute_url() + "#comentarios")
        return self.render_to_response(self.get_context_data(form=form))


class ArgumentoCreateView(CreateView):
    model = Argumento
    form_class = ArgumentoForm
    template_name = "debate/argumento_form.html"

    def get_initial(self):
        initial = super().get_initial()
        # permite links do tipo /argumentos/novo/?politico=1&posicao=D
        for campo in ("politico", "posicao", "tema"):
            if self.request.GET.get(campo):
                initial[campo] = self.request.GET[campo]
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Argumento criado com sucesso!")
        return super().form_valid(form)


class ArgumentoUpdateView(UpdateView):
    model = Argumento
    form_class = ArgumentoForm
    template_name = "debate/argumento_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Argumento atualizado!")
        return super().form_valid(form)


class ArgumentoDeleteView(DeleteView):
    model = Argumento
    template_name = "debate/confirmar_exclusao.html"
    success_url = reverse_lazy("debate:argumento_lista")

    def form_valid(self, form):
        messages.success(self.request, "Argumento excluído.")
        return super().form_valid(form)


# ---------- Políticos (CRUD completo) ----------

class PoliticoListView(ListView):
    model = Politico
    template_name = "debate/politico_lista.html"
    context_object_name = "politicos"


class PoliticoDetailView(DetailView):
    model = Politico
    template_name = "debate/politico_detalhe.html"
    context_object_name = "politico"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        args = self.object.argumentos.select_related("tema")
        ctx["defesas"] = args.filter(posicao=Argumento.DEFESA)
        ctx["criticas"] = args.filter(posicao=Argumento.CRITICA)
        return ctx


class PoliticoCreateView(CreateView):
    model = Politico
    form_class = PoliticoForm
    template_name = "debate/politico_form.html"


class PoliticoUpdateView(UpdateView):
    model = Politico
    form_class = PoliticoForm
    template_name = "debate/politico_form.html"


class PoliticoDeleteView(DeleteView):
    model = Politico
    template_name = "debate/confirmar_exclusao.html"
    success_url = reverse_lazy("debate:politico_lista")


def excluir_comentario(request, pk):
    """Remove um comentário (apenas via POST)."""
    from .models import Comentario

    comentario = get_object_or_404(Comentario, pk=pk)
    argumento = comentario.argumento
    if request.method == "POST":
        comentario.delete()
        messages.info(request, "Comentário removido.")
    return redirect(argumento.get_absolute_url() + "#comentarios")
