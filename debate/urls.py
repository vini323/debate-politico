from django.urls import path

from . import views

app_name = "debate"

urlpatterns = [
    path("", views.InicioView.as_view(), name="inicio"),

    # Argumentos
    path("argumentos/", views.ArgumentoListView.as_view(), name="argumento_lista"),
    path("argumentos/novo/", views.ArgumentoCreateView.as_view(), name="argumento_novo"),
    path("argumentos/<int:pk>/", views.ArgumentoDetailView.as_view(), name="argumento_detalhe"),
    path("argumentos/<int:pk>/editar/", views.ArgumentoUpdateView.as_view(), name="argumento_editar"),
    path("argumentos/<int:pk>/excluir/", views.ArgumentoDeleteView.as_view(), name="argumento_excluir"),

    # Políticos
    path("politicos/", views.PoliticoListView.as_view(), name="politico_lista"),
    path("politicos/novo/", views.PoliticoCreateView.as_view(), name="politico_novo"),
    path("politicos/<int:pk>/", views.PoliticoDetailView.as_view(), name="politico_detalhe"),
    path("politicos/<int:pk>/editar/", views.PoliticoUpdateView.as_view(), name="politico_editar"),
    path("politicos/<int:pk>/excluir/", views.PoliticoDeleteView.as_view(), name="politico_excluir"),

    # Comentários
    path("comentarios/<int:pk>/excluir/", views.excluir_comentario, name="comentario_excluir"),
]
