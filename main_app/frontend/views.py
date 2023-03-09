import os

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, resolve_url
from django.views import View
from django.shortcuts import render, redirect

from .forms import LoginUserForm
from .utils import BaseMixin


class LoginUser(LoginView):
    """
    Login user on start page (url 'login')
    """
    form_class = LoginUserForm
    template_name = 'frontend/login.html'

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)


def logout_user(request):
    """
    Logout user and redirect on start page
    """
    logout(request)
    return redirect('login')


class Schemas(View, BaseMixin):
    """
    Get info about created schemas and send ger on the html page
    """
    context = {}

    def get(self, request):
        self.context['schemas_list'] = self.get_current_schemas(str(request.user))
        return render(request, 'frontend/schemas.html', context=self.context)


class OneSchemas(View, BaseMixin):
    """
    Page with actions for one schema
    """
    context = {}

    def get(self, request, name):
        self.context['name'] = name
        self.context['schema_info'] = self.get_schema_info(name, str(request.user))
        self.context['user'] = str(request.user)
        self.context['data_schemas'] = self.get_data_schemas(name, str(request.user))

        return render(request, 'frontend/one_scheme.html', context=self.context)


class EditScheme(View, BaseMixin):
    """
    Page edit scheme (add or remove columns)
    """
    context = {}

    def get(self, request, name):
        self.context['name'] = name
        if name != 'new_schema':
            self.context['schema_info'] = self.get_schema_info(name, str(request.user))
        return render(request, 'frontend/edit_schema.html', context=self.context)

    def post(self, request, name):
        answer = self.save_schema(dict(request.POST), str(request.user))
        return redirect('schemas')


class DeleteScheme(View, BaseMixin):
    def get(self, request, name):
        answer = self.delete_schema(name, str(request.user))
        return redirect('schemas')