from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

class Empleado(AbstractUser):
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     return reverse('home:detalle_empleado', kwargs={'empleado_slug':self.empleado.slug})

    class Meta(AbstractUser.Meta):
        ordering = ['-username']
        verbose_name_plural = 'Empleados de Sermul'

def create_slug_empleado(instance, new_slug=None):
    slug = slugify(instance.username)
    if new_slug is not None:
        slug = new_slug
    qs = Empleado.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_empleado(instance, new_slug=new_slug)
    return slug

def pre_save_empleado_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_empleado(instance)

pre_save.connect(pre_save_empleado_receiver, sender=Empleado)

# @python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(_('Name'), max_length=150)
    slug = models.SlugField(unique=True)
    f_surname = models.CharField(_('First Surname'), max_length=150)
    s_maternal = models.CharField(_('Surname Maternal'), max_length=150)
    fecha_nac = models.DateField(verbose_name=_('Fecha de Nacimiento'), null=True,blank=True)
    avatar = models.ImageField(_('Image'), max_length=150)

    def get_absolute_url(self):
        return reverse('home:detalle_userprofile', kwargs={'pk':self.user.pk,'profile_slug':self.slug})

def create_slug_perfil(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = UserProfile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_perfil(instance, new_slug=new_slug)
    return slug

def pre_save_perfil_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_perfil(instance)

pre_save.connect(pre_save_perfil_receiver, sender=UserProfile)
