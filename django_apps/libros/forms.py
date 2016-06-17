from django import forms
from django.forms import ModelForm

from .models import DatosLibros, TipoLibro

class DatosLibrosForm(ModelForm):
    class Meta:
        model = DatosLibros
        fields = ['tipo_libro', 'num_serie', 'num_paginas', 'fecha_leg',
                  'fecha_mod', 'num_hojas', 'fecha_vence']

class TipoLibroForm(ModelForm):
    class Meta:
        model = TipoLibro
        fields = ['cliente', 'r_compras', 'r_ventas', 'lib_dia', 'lib_may',
                  'lib_inv_bal']

