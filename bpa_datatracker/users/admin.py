# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from import_export import resources, fields, widgets
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm


class UserWidget(widgets.ForeignKeyWidget):
    def __init__(self):
        self.model = User
        self.field = "username"
        self.username = ""
        self.firstname = ""
        self.lastname = ""

    def _set_name(self, name_from_source):
        # Use first letter from first name and whole of last name.

        parts = name_from_source.lower().split()
        if len(parts) >= 2:
            self.firstname = parts[0]
            self.lastname = parts[-1]
            self.username = self.firstname[0] + self.lastname
        else:
            self.firstname = parts[0]
            self.lastname = parts[0]
            self.username = self.lastname


    def clean(self, value):
        self._set_name(value)

        user, _ = self.model.objects.get_or_create(
                first_name=self.firstname,
                last_name=self.lastname,
                username=self.username)

        return user
