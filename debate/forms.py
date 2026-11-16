from django import forms

from .models import Argumento, Comentario, Politico


class PoliticoForm(forms.ModelForm):
    class Meta:
        model = Politico
        fields = ["nome", "partido", "cargo", "periodo", "biografia", "foto_url"]
        widgets = {"biografia": forms.Textarea(attrs={"rows": 4})}


class ArgumentoForm(forms.ModelForm):
    class Meta:
        model = Argumento
        fields = ["politico", "tema", "posicao", "titulo", "texto", "fonte", "autor"]
        widgets = {
            "texto": forms.Textarea(attrs={"rows": 6}),
            "posicao": forms.RadioSelect,
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["autor", "texto", "concorda"]
        widgets = {"texto": forms.Textarea(attrs={"rows": 3})}
