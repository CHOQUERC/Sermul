from django.conf.urls import url
from . import views

app_name = 'clientes'

urlpatterns = [
    url(r'^(?P<empleado_slug>[\w-]+)/$', views.ListarClientes.as_view(), name='clientes'),
    url(r'^crear/(?P<empleado_slug>[\w-]+)/$', views.CrearCliente.as_view(), name='crear_cliente'),
    url(r'^(?P<cliente_slug>[\w-]+)/eliminar/$', views.EliminarCliente.as_view(), name='eliminar_cliente'),
    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/editar/$', views.EditarCliente.as_view(), name='editar_cliente'),
    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/$', views.DetalleCliente.as_view(), name='detalle_cliente'),
]
