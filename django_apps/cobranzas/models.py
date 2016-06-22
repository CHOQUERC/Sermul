#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_apps.clientes.models import Cliente
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django_apps.home.models import Empleado

class Cobro(models.Model):
    MES = (
        ('Enero','Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo','Marzo'),
        ('Abril','Abril'),
        ('Mayo','Mayo'),
        ('Junio','Junio'),
        ('Julio','Julio'),
        ('Agosto','Agosto'),
        ('Septiembre','Septiembre'),
        ('Octubre','Octubre'),
        ('Noviembre','Noviembre'),
        ('Diciembre','Diciembre'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    decl_men = models.CharField(_('Declaración Mensual'), max_length=200)
    slug = models.SlugField(unique=True)
    planilla = models.CharField(_('Planilla'), max_length=200)
    balanc_gen = models.CharField(_('Balance General'), max_length=200)
    descripcion = models.CharField(_('Detalle del Cobro'), max_length=200)
    fecha_pago = models.DateField(_('Fecha de Pago'))
    monto = models.DecimalField(_('Monto S/.'), max_digits=16, decimal_places=2)
    periodo = models.CharField(_('Periodo'), choices=MES, max_length=10)
    anio = models.CharField(_('Año'), max_length=4)

    def __str__(self):
        return "%s: %s" %(self.empleado.username,self.cliente.usuario)

    def get_absolute_url(self):
        return reverse('cobranzas:detalle_cobro', kwargs={'empleado_slug':self.cliente.empleado.slug,'cliente_slug':self.cliente.slug,'cobro_slug':self.slug})

def create_slug_cobro(instance, new_slug=None):
    slug = slugify(instance.decl_men)
    if new_slug is not None:
        slug = new_slug
    qs = Cobro.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_cobro(instance, new_slug=new_slug)
    return slug

def pre_save_cobro_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_cobro(instance)

pre_save.connect(pre_save_cobro_receiver, sender=Cobro)

class Servicio(models.Model):
    cobro = models.ForeignKey(Cobro, on_delete=models.CASCADE)
    nombre = models.CharField(_('Nombre'), max_length=100)
    precio = models.IntegerField(_('Precio'))

    def __str__(self):
        return self.nombre
