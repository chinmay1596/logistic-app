import re

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.serializers import serialize
from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm
from django.forms.fields import Field
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView, BaseUpdateView
from django.views.generic.list import BaseListView

from apps.commons.mixins.file_export import ExportToExcel
from apps.commons.mixins.file_import import NormalFileImportMixin


class CustomSuccessMessageMixin(SuccessMessageMixin):
    object = None
    success_message = ''

    def perform_save(self, form):
        self.object = form.save()

    def send_success_message(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

    def form_valid(self, form):
        self.perform_save(form)
        self.send_success_message(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class LoginAndPermissionMixin(CustomSuccessMessageMixin, AccessMixin):
    _type = None
    login_required_message = 'Login Required'
    permission_denied_message = 'Permission Denied'
    login_required = getattr(settings, 'LOGIN_REQUIRED', False)
    permission_required = []

    def dispatch(self, request, *args, **kwargs):
        if self.login_required and request.user.is_authenticated and not request.user.is_active:
            return self._logout_user(request)
        if self.login_required and not request.user.is_authenticated:
            self._type = 'authentication'
            return self.handle_no_permission()
        elif self.permission_required and not self.has_permission():
            self._type = 'permission'
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    @staticmethod
    def _logout_user(request):
        auth_logout(request)
        return HttpResponseRedirect(getattr(settings, 'LOGOUT_REDIRECT_URL', settings.LOGIN_URL))

    def get_permission_denied_message(self):
        message = {
            'permission': self.permission_denied_message,
            'authentication': self.login_required_message
        }
        return message.get(self._type)


class CustomCreateView(LoginAndPermissionMixin, CreateView):
    pass


class CustomListView(LoginAndPermissionMixin, ListView):
    pass


class CustomUpdateView(LoginAndPermissionMixin, UpdateView):
    pass


class CustomDeleteView(LoginAndPermissionMixin, DeleteView):
    pass


class CustomDetailView(LoginAndPermissionMixin, DetailView):
    pass


class CustomExportView(LoginAndPermissionMixin, ExportToExcel):
    """
    This mixin is used to export data into excel file.
    To request for export file one must use get method.

    Required parameters:
    1. related_names = {'display_name': 'database_field'}
    2. queryset = Default queryset

    """
    pass


class CustomImportView(LoginAndPermissionMixin, NormalFileImportMixin):
    pass


class BaseAjaxBasedViewMixin:
    object = None

    def perform_create(self, form):
        self.object = form.save()

    def form_valid(self, form):
        self.perform_create(form)
        serialized_object = serialize('json', self.object.fields)
        return JsonResponse({'instance': serialized_object}, status=200)

    @staticmethod
    def form_invalid(form):
        return JsonResponse({'errors': form.errors}, status=400)

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return JsonResponse({'detail': self.get_permission_denied_message()}, status=403)


class ListWithFilterAndSearchMixin(LoginAndPermissionMixin, ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class CustomAjaxCreateView(BaseAjaxBasedViewMixin, LoginAndPermissionMixin, BaseCreateView):
    """Used for ajax data upload"""
    http_method_names = ['post', 'head', 'options', 'trace']


class CustomAjaxUpdateView(BaseAjaxBasedViewMixin, LoginAndPermissionMixin, BaseUpdateView):
    """
    reference for ajax post:
    https://www.pluralsight.com/guides/work-with-ajax-django
    """
    http_method_names = ['post', 'put', 'patch', 'head', 'options', 'trace']


class CustomAjaxListView(BaseAjaxBasedViewMixin, LoginAndPermissionMixin, BaseListView):
    object_list = None
    context_object_name = None
    allow_empty_first_page = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'previous_page': f'?page={page.previous_page_number()}' if page.has_previous() else None,
                'next_page': f'?page={page.next_page_number()}' if page.has_next() else None,
                'current_page': page.number,
                'is_paginated': is_paginated,
            }
        else:
            context = {
                'previous_page': None,
                'next_page': None,
                'current_page': 1,
                'is_paginated': False,
            }

        context.update({
            'results': list(
                map(
                    lambda x: x.to_dict(),
                    queryset
                )
            )
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return JsonResponse(self.get_context_data(), safe=False)


class CustomAjaxDetailView(BaseAjaxBasedViewMixin, LoginAndPermissionMixin, BaseDetailView):

    def get_context_object_name(self, obj):
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return JsonResponse(self.object.to_dict(), safe=False)


class DynamicFieldsModelForm(ModelForm):
    def __init__(self, fields=None, exclude_fields=None, non_required_fields=None, hidden_fields=None, **kwargs):
        super().__init__(**kwargs)
        if exclude_fields:
            assert isinstance(exclude_fields, list), 'Exclude Fields must be list'
            self._exclude_fields(exclude_fields)
        elif fields:
            assert isinstance(fields, list), 'Fields must be list'
            self._new_fields(fields)
        self.set_non_required_fields()
        self.set_hidden_fields()
        # self.set_readonly_fields()
        self.set_placeholder()
        self.set_field_class()

    def _exclude_fields(self, fields):
        for field in fields:
            _ = self.fields.pop(field, None)

    def _new_fields(self, fields):
        existing_fields = set(self.fields.keys())
        deleted_fields = existing_fields - set(fields)
        self._exclude_fields(deleted_fields)

    def set_non_required_fields(self):
        non_required_fields = getattr(self.__class__.Meta, 'non_required_fields', [])
        if non_required_fields:
            for key in non_required_fields:
                self.fields[key].widget.attrs['readonly'] = True

    # def set_readonly_fields(self):
    #     readonly_fields = getattr(self.__class__.Meta, 'readonly_fields', [])
    #     print(self.fields.keys())
    #     if readonly_fields:
    #         for key in readonly_fields:
    #             self.fields[key].required = False

    def set_hidden_fields(self):
        hidden_fields = getattr(self.__class__.Meta, 'hidden_fields', [])
        if hidden_fields:
            for key in hidden_fields:
                self.fields[key].widget.attrs.update({'hidden': True})

    def set_placeholder(self):
        placeholders = getattr(self.__class__.Meta, 'placeholder', None)
        if placeholders:
            for key, placeholder in placeholders.items():
                self.fields[key].widget.attrs.update({'placeholder': placeholder})

    def set_field_class(self):
        class_map = getattr(self.__class__.Meta, 'class_map', None)
        if class_map:
            for key, _class in class_map.items():
                if isinstance(_class, list):
                    _class = ' '.join(_class)
                assert isinstance(_class, str), "Classes must be either string or list."
                self.fields[key].widget.attrs.update({'class': _class})


class CommaSeparatedEmailField(Field):
    description = _(u"E-mail address(es)")

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ",")
        super(CommaSeparatedEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):
        """
        Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        """
        value = self.to_python(value)

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError(_(u"This field is required."))

        email_re = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        for email in value:
            if not email_re.match(email):
                raise forms.ValidationError(_(u"'%s' is not a valid "
                                              "e-mail address.") % email)
        return value
