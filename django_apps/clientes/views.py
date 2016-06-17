from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django_apps.home.models import Empleado
from .models import Cliente
from .forms import ClienteForm

class CrearCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    slug_url_kwarg = 'cliente_slug'
    template_name = 'clientes/crear_cliente.html'
    def get_empleado(self):
        return get_object_or_404(Empleado, slug=self.kwargs.get('empleado_slug'))

    def get_initial(self):
        initial = super(CreateView,self).get_initial()
        initial['empleado'] = self.get_empleado()
        return initial

class EditarCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    slug_url_kwarg = 'cliente_slug'
    template_name = 'clientes/crear_cliente.html'

class DetalleCliente(DetailView):
    model = Cliente
    slug_url_kwarg = 'cliente_slug'
    template_name = 'clientes/detalle_cliente.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleCliente, self).get_context_data(**kwargs)
        context['ahora'] = timezone.now()
        return context

class ListarClientes(ListView):
    model = Cliente
    paginate_by = 6
    context_object_name = 'list_clientes'
    template_name = 'clientes/listar_clientes.html'

class EliminarCliente(DeleteView):
    model = Cliente
    slug_url_kwarg = 'cliente_slug'
    template_name = 'clientes/confirmar_eliminar_cliente.html'
    success_url = reverse_lazy('clientes:clientes')

