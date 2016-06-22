#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django_apps.clientes.models import Cliente

class UIT(models.Model):
    UIT = (
        ('UIT 150', 'UIT 150'),
        ('UIT 500', 'UIT 500'),
        ('UIT 1700', 'UIT 1700'),
        ('UIT > 1700', 'UIT > 1700'),
    )
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    uit = models.CharField(_('UIT'), max_length=10, choices=UIT, default='UIT 150')

    def __str__(self):
        return cliente.r_social

    def get_absolute_url(self):
        return reverse('libros:detalle_libros', kwargs={'empleado_slug':self.cliente.empleado.slug,'cliente_slug':self.cliente.slug,'uit_pk':self.pk})

class TipoLibro(models.Model):
    TIPO = (
        ('Registro de Compras', 'Registro de Compras'),
        ('Registro de Ventas', 'Registro de Ventas'),
        ('Libro Diario', 'Libro Diario'),
        ('Libro Mayor', 'Libro Mayor'),
        ('Libro de Inventario y Balances','Libro de Inventario y Balances'),
        ('Libro Caja Banco', 'Libro Caja Banco'),
        ('Libro Diario Simplificado','Libro Diario Simplificado'),
        ('Libro de Retenciones','Libro de Retenciones'),
        ('Registro de activos fijos','Registro de activos fijos'),
        ('Registro de Costos','Registro de Costos'),
        ('Registro de Inventario permanente de unidades físicas','Registro de Inventario permanente de unidades físicas'),
        ('Registro de Inventario permanente Valorizado','Registro de Inventario permanente Valorizado'),
    )
    uit = models.ForeignKey(UIT, on_delete=models.CASCADE)
    #UIT 150
    libro = models.CharField(_('Libro de Contabilidad'),max_length=54,choices=TIPO)
    num_serie = models.PositiveIntegerField(_('Número de Serie'))
    num_paginas = models.PositiveIntegerField(_('Número de Paginas'))
    fecha_leg = models.DateField(_('Fecha de Legalización'))
    fecha_mod = models.DateField(_('Fecha de Modificación'))
    num_hojas = models.PositiveIntegerField(_('Número de hojas'))
    fecha_vence = models.DateField(_('Fecha de Vencimiento'))

    def __str__(self):
        return self.num_serie

