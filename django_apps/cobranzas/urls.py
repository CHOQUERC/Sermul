# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

app_name = 'cobranzas'

urlpatterns = [

    url('(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/nuevo-cobro/$', views.CrearCobro.as_view(), name='nuevo_cobro'),
    url('(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/(?P<cobro_slug>[\w-]+)/eliminar/$', views.EliminarCobro.as_view(), name='eliminar_cobro'),
    # EDITAR COBRO
    url('(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/(?P<cobro_slug>[\w-]+)/editar/$', views.EditarCobro.as_view(), name='editar_cobro'),
    # DETALLE COBRO
    url('(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/(?P<cobro_slug>[\w-]+)/$', views.DetalleCobro.as_view(), name='detalle_cobro'),
    # NUEVO COBRO
    # ELMINAR COBRO
    # LISTAR COBRO
    url('(?P<empleado_slug>[\w-]+)/(?P<cliente_slug>[\w-]+)/$', views.ListaCobros.as_view(), name='listar_cobros'),


]
