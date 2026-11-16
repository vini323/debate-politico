from django.contrib import admin

from .models import Argumento, Comentario, Politico, Tema


class ArgumentoInline(admin.TabularInline):
    model = Argumento
    extra = 0
    fields = ("titulo", "posicao", "tema", "autor")
    show_change_link = True


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ("autor", "texto", "concorda", "aprovado")


@admin.register(Politico)
class PoliticoAdmin(admin.ModelAdmin):
    list_display = ("nome", "partido", "cargo", "periodo", "total_defesas", "total_criticas")
    search_fields = ("nome", "partido")
    inlines = [ArgumentoInline]

    @admin.display(description="defesas")
    def total_defesas(self, obj):
        return obj.total_defesas

    @admin.display(description="críticas")
    def total_criticas(self, obj):
        return obj.total_criticas


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Argumento)
class ArgumentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "politico", "posicao", "tema", "autor", "criado_em")
    list_filter = ("politico", "posicao", "tema")
    search_fields = ("titulo", "texto", "autor")
    date_hierarchy = "criado_em"
    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("autor", "argumento", "concorda", "aprovado", "criado_em")
    list_filter = ("aprovado", "concorda", "argumento__politico")
    list_editable = ("aprovado",)
    search_fields = ("autor", "texto")
    actions = ["aprovar", "reprovar"]

    @admin.action(description="Aprovar comentários selecionados")
    def aprovar(self, request, queryset):
        queryset.update(aprovado=True)

    @admin.action(description="Ocultar comentários selecionados")
    def reprovar(self, request, queryset):
        queryset.update(aprovado=False)
