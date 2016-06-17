#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import UserChangeForm
from .models import Empleado


class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Empleado
        fields = ['username','password','email']


class CreateUserForm(ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label=" Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label=" Confirm Password")
    #Esta función clean_password(self) verifica que las contraseñas sean iguales
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2  and password1 != password2:
            raise forms.ValidationError("Los Passwords no son iguales")
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = Empleado
        fields = ('username','email')
