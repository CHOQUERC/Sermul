#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.template import RequestContext # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django_apps.home.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Cobro, Servicio
from .forms import CobroForm, ServicioForm, ServicioFormSet

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

def NuevoCobro(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    ServicioFormset = formset_factory(ServicioForm, max_num=10, formset=RequiredFormSet, min_num=1, validate_min=True, extra=1)

    if request.method == 'POST': # If the form has been submitted...
        cobro_form = CobroForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        servicio_formset = ServicioFormset(request.POST, request.FILES)

        if cobro_form.is_valid() and servicio_formset.is_valid():
            cobro = cobro_form.save()
            for form in servicio_formset.forms:
                servicio = form.save(commit=False)
                servicio.list = todo_list
                servicio.save()

            return HttpResponseRedirect(cobro.get_absolute_url()) # Redirect to a 'success' page
    else:
        cobro_form = CobroForm()
        servicio_formset = ServicioFormset()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
    c = {'form': cobro_form,
         'servicio_form': servicio_formset,
        }
    c.update(csrf(request))

    return render_to_response('cobranzas/nuevo_cobro.html', c,  context_instance=RequestContext(request))

class CrearCobro(CreateView,LoginRequiredMixin, SuccessMessageMixin):
    model = Cobro
    form_class = CobroForm
    slug_url_kwarg = 'cobro_slug'
    success_message = 'El Cobro se realizó con éxito'
    template_name = 'cobranzas/nuevo_cobro.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form = form,
                                                             servicio_form = servicio_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioFormSet(self.request.POST)
        if (form.is_valid() and servicio_form.is_valid()):
            return self.form_valid(form, servicio_form)
        else:
            return self.form_invalid(form, servicio_form)

    def form_valid(self, form, servicio_form):
        self.object = form.save()
        for form in servicio_form.forms:
            servicio_form.instance = self.object
            servicio_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, servicio_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  servicio_form=servicio_form)
        )
    # def get_context_data(self, **kwargs):
    #     context = super(CrearCobro, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['formset'] = ServicioFormSet(self.request.POST)
    #     else:
    #         context['formset'] = ServicioFormSet()
    #     return context

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['formset']
    #     if formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return redirect(self.object.get_absolute_url())  # assuming your model has ``get_absolute_url`` defined.
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form))

class EditarCobro(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cobro
    form_class = CobroForm
    slug_url_kwarg = 'cobro_slug'
    success_message = 'El Cobro se ha editado con éxito'
    template_name = 'cobranzas/nuevo_cobro.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form = form,
                                                             servicio_form = servicio_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and servicio_form.is_valid()):
            return self.form_valid(form, servicio_form)
        else:
            return self.form_invalid(form, servicio_form)

    def form_valid(self, form, servicio_form):
        self.object = form.save()
        servicio_form.instance = self.object
        servicio_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, servicio_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  servicio_form=servicio_form)
        )

class ListaCobros(LoginRequiredMixin, ListView):
    model = Cobro
    context_object_name = 'listar_cobros'
    template_name = 'cobranzas/listar_cobros.html'
    paginate_by = 10

class DetalleCobro(LoginRequiredMixin, DetailView):
    model = Cobro
    template_name = 'cobranzas/detalle_cobro.html'
    slug_url_kwarg = 'cobro_slug'

    def get_context_data(self, **kwargs):
        context = super(DetalleCobro, self).get_context_data(**kwargs)
        context['servicios'] = Servicio.objects.all()
        return context

class EliminarCobro(LoginRequiredMixin, DeleteView):
    model = Cobro
    slug_url_kwarg = 'cobro_slug'
    template_name = 'cobranzas/confirmar_eliminar_cobro.html'

    def get_success_url(self):
        return reverse('cobranzas:listar_cobros', kwargs={'empleado_slug':self.object.cliente.empleado.slug,'cliente_slug':self.object.cliente.slug})
