from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic import *
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.template import RequestContext # For CSRF
from django.core.urlresolvers import reverse_lazy, reverse
from django_apps.home.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django_apps.clientes.models import Cliente
from .models import UIT, TipoLibro
from .forms import UITForm, TipoLibroForm


class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        self.validate_unique()
        if any(self.errors):
            return
        if not self.forms[0].has_changed():
            raise forms.ValidationError("At least one %s is required" % self.model._meta.verbose_name)

@login_required(login_url='home:login_user')
def CreateLibros(request,empleado_slug=None,cliente_slug=None):
    uit_form = UITForm(request.POST or None)
    TipoLibroFormSet = inlineformset_factory(UIT, TipoLibro, form=TipoLibroForm,formset=RequiredBaseInlineFormSet, max_num=12, extra=1)
    tipolibro_formset = TipoLibroFormSet(request.POST or None, prefix='tipolibro')
    if uit_form.is_valid() and tipolibro_formset.is_valid():
        uit = uit_form.save()
        tipolibro = tipolibro_formset.save(commit=False)
        for lib in tipolibro:
            lib.uit = uit
            lib.save()
        messages.add_message(request, messages.INFO, 'Se ha registrado correctamente')
        return HttpResponseRedirect(uit.get_absolute_url())
    return render_to_response(
        'libros/libro_form.html', {
            'form': uit_form,
            'formset':tipolibro_formset,
        }, context_instance = RequestContext(request)
    )

@login_required(login_url='home:login_user')
def UpdateLibros(request,empleado_slug=None,cliente_slug=None,uit_pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = UIT.objects.get(pk=uit_pk)
    uit_form = UITForm(request.POST or None, instance=instance)
    TipoLibroFormSet = inlineformset_factory(UIT, TipoLibro, form=TipoLibroForm,formset=RequiredBaseInlineFormSet, max_num=12, extra=1)
    tipolibro_formset = TipoLibroFormSet(request.POST or None, prefix='tipolibro', instance=instance)
    if uit_form.is_valid() and tipolibro_formset.is_valid():
        uit = uit_form.save()
        tipolibro = tipolibro_formset.save(commit=False)
        for lib in tipolibro:
            lib.uit = uit
            lib.save()
        messages.add_message(request, messages.INFO, 'Se ha editado correctamente')
        return HttpResponseRedirect(uit.get_absolute_url())
    return render_to_response(
        'libros/libro_form.html', {
            'form': uit_form,
            'formset':tipolibro_formset,
        }, context_instance = RequestContext(request)
    )

class DetalleDatosLibros(DetailView):
    model = UIT
    pk_url_kwarg = 'uit_pk'
    template_name = 'libros/detalle_datoslibros.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleDatosLibros, self).get_context_data(**kwargs)
        context['libros'] = TipoLibro.objects.filter(uit_id=self.object.id)
        return context

class ListarDatosLibros(ListView):
    model = UIT
    paginate_by = 6
    slug_url_kwarg = 'cliente_slug'
    context_object_name = 'list_libros'
    template_name = 'libros/listar_datoslibros.html'

    def get_context_data(self, **kwargs):
        context = super(ListarDatosLibros, self).get_context_data(**kwargs)
        context['cliente'] = Cliente.objects.get(slug=self.kwargs['cliente_slug'])
        context['libros'] = TipoLibro.objects.all()
        return context

class EliminarDatosLibros(DeleteView):
    model = UIT
    pk_url_kwarg = 'uit_pk'
    template_name = 'libros/confirmar_eliminar_datoslibros.html'

    def get_success_url(self):
        return reverse('libros:listar_libros', kwargs={'empleado_slug':self.object.cliente.empleado.slug,'cliente_slug':self.object.cliente.slug})
