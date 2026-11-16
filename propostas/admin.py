from django.contrib import admin

from .models import Candidato, Proposta, Tema


class PropostaInline(admin.TabularInline):
    model = Proposta
    extra = 0
    fields = ("tema", "titulo", "depende_congresso")
    show_change_link = True


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ("nome_urna", "numero", "partido", "vice", "total_propostas")
    search_fields = ("nome", "nome_urna", "partido")
    inlines = [PropostaInline]

    @admin.display(description="propostas")
    def total_propostas(self, obj):
        return obj.propostas.count()


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("nome", "icone", "ordem", "total_propostas")
    list_editable = ("ordem",)
    search_fields = ("nome",)

    @admin.display(description="propostas")
    def total_propostas(self, obj):
        return obj.propostas.count()


@admin.register(Proposta)
class PropostaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "candidato", "tema", "depende_congresso", "atualizado_em")
    list_filter = ("candidato", "tema", "depende_congresso")
    search_fields = ("titulo", "descricao")
    list_select_related = ("candidato", "tema")
