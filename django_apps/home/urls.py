# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.urlresolvers import reverse_lazy
from . import views

app_name = 'home'

urlpatterns = [
    ## Gestion de usuarios
    url(r'^sermul/$', views.ControlPanelSermul.as_view(), name='inicio'),
    url(r'^usuarios/$', views.ListUsers.as_view(), name='listar_usuarios'),
    url(r'^signup/$', views.UserCreate.as_view(), name='signup_user'),
    url(r'^login/$', views.Login.as_view(), name='login_user'),
    url(r'^logout/$', views.Logout.as_view(), name='logout_user'),

    #Cambiar Usuario creado
    # url(r'^usuario/(?P<pk>[0-9]+)/editar/$', views.EditUser,
    #     name="editar_user"),
    url(r'^usuario/(?P<empleado_slug>[\w-]+)/editar/$', views.EditUser.as_view(),
        name="editar_user"),

    # Cambiar Contraseña de usuario
    # url(r'^usuarios/', include('django.contrib.auth.urls')),
    url(r'^usuario/(?P<empleado_slug>[\w-]+)/password_change/$', views.password_change,
        name="password_change"),

    ## Gestion de perfiles de usuarios
    url(r'^usuario/(?P<pk>[0-9]+)/perfil/editar/$', views.EditUserProfile.as_view(), name='editar_userprofile'),
    url(r'^usuario/(?P<pk>[0-9]+)/perfil/(?P<profile_slug>[\w-]+)/$', views.DetailUserProfile.as_view(), name='detalle_userprofile'),

]
