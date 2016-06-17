from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Cliente(models.Model):
    ESTADO = (
        ('Activo', 'Activo'),
        ('Suspencion', 'Suspencion',),
        ('Baja', 'Baja Definitiva'),
    )
    REGIMEN = (
        ('General', 'General'),
        ('Especial', 'Especial'),
    )
    empleado = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Empleado')
    slug = models.SlugField(unique=True)
    r_social = models.CharField(_('Razon Social'), max_length=100)
    ruc = models.CharField(_('RUC'), max_length=11)
    usuario = models.CharField(_('Usuario'), max_length=50)
    clave_sol = models.CharField(_('Clave Sol'), max_length=20)
    estado = models.CharField(_('Estado'), choices=ESTADO, max_length=10)
    regimen = models.CharField(_('Regimen'), choices=REGIMEN, max_length=8)

    def __str__(self):
        return self.r_social

    def get_absolute_url(self):
        return reverse('clientes:detalle_cliente', kwargs={'empleado_slug':self.empleado.slug,'cliente_slug':self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.usuario)
    if new_slug is not None:
        slug = new_slug
    qs = Cliente.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Cliente)
