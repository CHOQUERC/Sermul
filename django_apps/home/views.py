#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from django.conf import settings
from django.views.generic import FormView, TemplateView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import resolve_url
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from registration.signals import user_registered
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from .models import Empleado, UserProfile
from .forms import CreateUserForm, UserEditForm
from django_apps.clientes.models import Cliente
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

def setlanguage(request):
    context = {
        'LANGUAGES': settings.LANGUAGES,
        'SELECTEDLANG': request.LANGUAGE_CODE
    }
    return render(request, "set-languaje.html", context)

class Login(FormView):
    form_class = AuthenticationForm
    template_name = "home/login.html"
    success_url = reverse_lazy('home:inicio')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


class Logout(RedirectView):
    pattern_name = 'home:login_user'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)

class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home:login_user'))
        else:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class ControlPanelSermul(LoginRequiredMixin, TemplateView):
    template_name = 'base_sistema.html'
    def get_context_data(self, **kwargs):
        context = super(ControlPanelSermul, self).get_context_data(**kwargs)
        return context

class UserCreate(SuccessMessageMixin,FormView):
    model = Empleado
    form_class = CreateUserForm
    template_name = 'home/signup.html'
    success_url = reverse_lazy('home:login_user')
    success_message = 'El usuario %(username)s se ha creado correctamente'
    slug_url_kwarg = 'empleado_slug'

    def get_initial(self):
        logout(self.request)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = Empleado.objects.create_user(username,email,password)
            user.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def asegurar_existencia_perfil_user(pk):
    usuario = Empleado.objects.get(pk=pk)
    try:
        userprofile = usuario.userprofile
    except UserProfile.DoesNotExist, e:
        userprofile = UserProfile(user=usuario)
        userprofile.save()
    return userprofile

def crea_perfil_user(**kwargs):
    UserProfile.objects.get_or_create(user=kwargs['usuario'])

user_registered.connect(crea_perfil_user)

@login_required
def EditUser(request, slug=None):
    """
    Editar usuario de forma simple.
    """
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            #Actualizar el objeto
            user = form.save()
            messages.success(request, 'Usuario actualizado exitosamente.', extra_tags='html_dante')
            return HttpResponseRedirect(reverse('home:listar_usuarios'))
    else:
        form = UserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'home/user_change.html', context)

class EditUser(UpdateView):
    model = Empleado
    form_class = UserEditForm
    template_name = 'home/user_change.html'
    slug_url_kwarg = 'empleado_slug'

    def get_success_url(self):
        return reverse('home:listar_usuarios')

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(EditUser, self).dispatch(*args, **kwargs)

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='home/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    empleado_slug=None,
                    extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('home:login_user')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            messages.success(request, _('Contrasena cambiado correctamente'),extra_tags='html_dante')
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class ListUsers(LoginRequiredMixin,ListView):
    model = Empleado
    context_object_name = 'list_users'
    template_name = 'home/listar_usuarios.html'

    def get_context_data(self, **kwargs):
        context = super(ListUsers, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        return context
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(ListUsers, self).dispatch(*args, **kwargs)

class DeleteUser(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Empleado
    slug_url_kwarg = 'empleado_slug'
    success_message = 'El usuario %(username)s fue eliminado correctamente'
    template_name = 'home/confirmar_eliminar_usuario.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteUser, self).delete(request, *args, **kwargs)

class EditUserProfile(LoginRequiredMixin,UpdateView):
    model = UserProfile
    template_name = 'home/form_userprofile.html'
    fields = ['name', 'f_surname', 's_maternal', 'fecha_nac','avatar']
    slug_url_kwarg = 'profile_slug'
    # pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        asegurar_existencia_perfil_user(self.kwargs['pk'])
        return (super(EditUserProfile, self).get(self, request, *args, **kwargs))

class DetailUserProfile(LoginRequiredMixin,DetailView):
    model = UserProfile
    # slug_url_kwarg = 'profile_slug'
    template_name = 'home/detail_userprofile.html'
