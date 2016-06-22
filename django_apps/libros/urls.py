# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'libros'

urlpatterns = [
    url(r'^(?P<empleado_slug>[\w]+)/(?P<cliente_slug>[\w-]+)/crear-libro/$', views.CreateLibros, name='crear_libros'),
    url(r'^(?P<empleado_slug>[\w]+)/(?P<cliente_slug>[\w-]+)/(?P<uit_pk>[0-9]+)/eitar-libros/$', views.UpdateLibros, name='editar_libros'),
    url(r'^(?P<empleado_slug>[\w]+)/(?P<cliente_slug>[\w-]+)/libros/$', views.ListarDatosLibros.as_view(), name='listar_libros'),
    url(r'^(?P<empleado_slug>[\w]+)/(?P<cliente_slug>[\w-]+)/(?P<uit_pk>[0-9]+)/$', views.DetalleDatosLibros.as_view(), name='detalle_libros'),
    url(r'^(?P<empleado_slug>[\w]+)/(?P<cliente_slug>[\w-]+)/(?P<uit_pk>[0-9]+)/eliminar-libros/$', views.EliminarDatosLibros.as_view(), name='eliminar_libros'),
]
