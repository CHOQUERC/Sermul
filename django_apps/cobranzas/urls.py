# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

app_name = 'cobranzas'

urlpatterns = [

    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/nuevo-cobro/$', views.CrearCobro, name='nuevo_cobro'),
    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/(?P<cobro_slug>[\w-]+)/eliminar/$', views.EliminarCobro.as_view(), name='eliminar_cobro'),
    # EDITAR COBRO
    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/(?P<cobro_slug>[\w-]+)/editar/$', views.EditarCobro, name='editar_cobro'),
    # DETALLE COBRO
    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/(?P<cobro_slug>[\w-]+)/$', views.DetalleCobro.as_view(), name='detalle_cobro'),
    # NUEVO COBRO
    # ELMINAR COBRO
    # LISTAR COBRO
    url(r'^(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/$', views.ListaCobros.as_view(), name='listar_cobros'),


]
