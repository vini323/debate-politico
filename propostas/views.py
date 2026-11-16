from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CandidatoForm, PropostaForm
from .models import Candidato, Proposta, Tema


# ---------- Página inicial ----------

class InicioView(ListView):
    """Os candidatos lado a lado e a lista de temas para comparar."""

    template_name = "propostas/inicio.html"
    context_object_name = "candidatos"

    def get_queryset(self):
        return Candidato.objects.annotate(n_propostas=Count("propostas")).order_by("nome_urna")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["temas"] = Tema.objects.annotate(n_propostas=Count("propostas")).order_by("ordem", "nome")
        return ctx


# ---------- Comparação por tema ----------

class TemaCompararView(DetailView):
    """Mostra, para um tema, as propostas de cada candidato em colunas."""

    model = Tema
    template_name = "propostas/tema_comparar.html"
    context_object_name = "tema"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        colunas = []
        for c in Candidato.objects.all():
            colunas.append({
                "candidato": c,
                "propostas": self.object.propostas.filter(candidato=c),
            })
        ctx["colunas"] = colunas
        ctx["temas"] = Tema.objects.all()
        return ctx


# ---------- Propostas (CRUD) ----------

class PropostaListView(ListView):
    model = Proposta
    template_name = "propostas/proposta_lista.html"
    context_object_name = "propostas"
    paginate_by = 15

    def get_queryset(self):
        qs = Proposta.objects.select_related("candidato", "tema")
        g = self.request.GET
        if g.get("candidato"):
            qs = qs.filter(candidato_id=g["candidato"])
        if g.get("tema"):
            qs = qs.filter(tema_id=g["tema"])
        if g.get("q"):
            qs = qs.filter(Q(titulo__icontains=g["q"]) | Q(descricao__icontains=g["q"]))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["candidatos"] = Candidato.objects.all()
        ctx["temas"] = Tema.objects.all()
        ctx["filtros"] = self.request.GET
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()
        return ctx


class PropostaDetailView(DetailView):
    model = Proposta
    template_name = "propostas/proposta_detalhe.html"
    context_object_name = "proposta"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # o que o(s) outro(s) candidato(s) propõe(m) no mesmo tema
        ctx["outras"] = (
            Proposta.objects.filter(tema=self.object.tema)
            .exclude(candidato=self.object.candidato)
            .select_related("candidato")
        )
        return ctx


class PropostaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proposta
    form_class = PropostaForm
    template_name = "propostas/proposta_form.html"
    success_message = "Proposta cadastrada!"

    def get_initial(self):
        initial = super().get_initial()
        for campo in ("candidato", "tema"):
            if self.request.GET.get(campo):
                initial[campo] = self.request.GET[campo]
        return initial


class PropostaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proposta
    form_class = PropostaForm
    template_name = "propostas/proposta_form.html"
    success_message = "Proposta atualizada!"


class PropostaDeleteView(LoginRequiredMixin, DeleteView):
    model = Proposta
    template_name = "propostas/confirmar_exclusao.html"
    success_url = reverse_lazy("propostas:proposta_lista")

    def form_valid(self, form):
        messages.success(self.request, "Proposta excluída.")
        return super().form_valid(form)


# ---------- Candidatos (CRUD) ----------

class CandidatoListView(ListView):
    model = Candidato
    template_name = "propostas/candidato_lista.html"
    context_object_name = "candidatos"

    def get_queryset(self):
        return Candidato.objects.annotate(n_propostas=Count("propostas")).order_by("nome_urna")


class CandidatoDetailView(DetailView):
    model = Candidato
    template_name = "propostas/candidato_detalhe.html"
    context_object_name = "candidato"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        grupos = []
        for tema in Tema.objects.all():
            props = self.object.propostas.filter(tema=tema)
            if props:
                grupos.append({"tema": tema, "propostas": props})
        ctx["grupos"] = grupos
        return ctx


class CandidatoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "propostas/candidato_form.html"
    success_message = "Candidato cadastrado!"


class CandidatoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "propostas/candidato_form.html"
    success_message = "Candidato atualizado!"


class CandidatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Candidato
    template_name = "propostas/confirmar_exclusao.html"
    success_url = reverse_lazy("propostas:candidato_lista")

    def form_valid(self, form):
        messages.success(self.request, "Candidato excluído.")
        return super().form_valid(form)
