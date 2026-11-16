from django import forms

from .models import Candidato, Proposta


class PropostaForm(forms.ModelForm):
    class Meta:
        model = Proposta
        fields = ["candidato", "tema", "titulo", "descricao", "depende_congresso", "fonte"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 6})}


class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = [
            "nome", "nome_urna", "numero", "partido", "coligacao", "vice",
            "titulo_plano", "resumo", "link_plano", "cor",
        ]
        widgets = {
            "resumo": forms.Textarea(attrs={"rows": 4}),
            "cor": forms.TextInput(attrs={"type": "color"}),
        }
