from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import inlineformset_factory
from .models import Cobro, Servicio

class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = ['cliente','decl_men','planilla','balanc_gen',
                  'descripcion','fecha_pago','monto','periodo']

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre','precio']

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

ServicioFormSet = inlineformset_factory(Cobro,Servicio,form=ServicioForm, extra=1, validate_max=10,min_num=1,max_num=10)
