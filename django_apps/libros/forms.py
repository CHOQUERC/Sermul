from django import forms
from django.forms import ModelForm

from .models import UIT, TipoLibro

class UITForm(ModelForm):
    class Meta:
        model = UIT
        fields = ['cliente','uit']

class TipoLibroForm(ModelForm):
    class Meta:
        model = TipoLibro
        fields = ['libro', 'num_serie', 'num_paginas', 'fecha_leg', 'fecha_mod',
                  'num_hojas','fecha_vence']

