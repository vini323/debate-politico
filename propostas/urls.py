from django.urls import path

from . import views

app_name = "propostas"

urlpatterns = [
    path("", views.InicioView.as_view(), name="inicio"),

    # Comparação lado a lado
    path("comparar/<int:pk>/", views.TemaCompararView.as_view(), name="tema_comparar"),

    # Propostas
    path("propostas/", views.PropostaListView.as_view(), name="proposta_lista"),
    path("propostas/nova/", views.PropostaCreateView.as_view(), name="proposta_nova"),
    path("propostas/<int:pk>/", views.PropostaDetailView.as_view(), name="proposta_detalhe"),
    path("propostas/<int:pk>/editar/", views.PropostaUpdateView.as_view(), name="proposta_editar"),
    path("propostas/<int:pk>/excluir/", views.PropostaDeleteView.as_view(), name="proposta_excluir"),

    # Candidatos
    path("candidatos/", views.CandidatoListView.as_view(), name="candidato_lista"),
    path("candidatos/novo/", views.CandidatoCreateView.as_view(), name="candidato_novo"),
    path("candidatos/<int:pk>/", views.CandidatoDetailView.as_view(), name="candidato_detalhe"),
    path("candidatos/<int:pk>/editar/", views.CandidatoUpdateView.as_view(), name="candidato_editar"),
    path("candidatos/<int:pk>/excluir/", views.CandidatoDeleteView.as_view(), name="candidato_excluir"),
]
