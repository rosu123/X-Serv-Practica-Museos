from django import forms
from django.forms import ModelForm

from museos.models import Museo


class nuevoComentario(forms.Form):
    museo = forms.ModelChoiceField(label='Museo', queryset=Museo.objects.order_by("nombre"))
    comentario = forms.CharField(label='Comentario',widget=forms.Textarea)
