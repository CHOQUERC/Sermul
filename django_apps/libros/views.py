from django.shortcuts import render
from django.views.generic import *
from django.utils import timezone
from .models import DatosLibros, TipoLibro
from .forms import DatosLibrosForm, TipoLibroForm

class CrearDatosLibros(CreateView):
    model = DatosLibros
    form_class = DatosLibrosForm
    template_name = 'libros/crear_datoslibros.html'

class EditarDatosLibros(UpdateView):
    model = DatosLibros
    form_class = DatosLibrosForm
    template_name = 'libros/crear_datoslibros.html'

class DetalleDatosLibros(DetailView):
    model = DatosLibros
    template_name = 'libros/detalle_datoslibros.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleDatosLibros, self).get_context_data(**kwargs)
        context['ahora'] = timezone.now()
        return context

class ListarDatosLibros(ListView):
    model = DatosLibros
    paginate_by = 6
    context_object_name = 'list_libros'
    template_name = 'libros/listar_datoslibros.html'

class EliminarDatosLibros(DeleteView):
    model = DatosLibros
    template_name = 'libros/confirmar_eliminar_datoslibros.html'
    success_url = reverse_lazy('libros:datos_libros')


