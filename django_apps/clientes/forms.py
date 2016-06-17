from django import forms
from django.forms import ModelForm

from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['empleado','r_social', 'ruc', 'usuario', 'clave_sol', 'estado', 'regimen']

