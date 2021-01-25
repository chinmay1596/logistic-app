from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from apps.commons.mixins.commons import DynamicFieldsModelForm, CommaSeparatedEmailField
from apps.employee.constants import ACTIVE
from apps.employee.models import UserInvite, Driver
from apps.orders.models import OrderBundle

UserModel = get_user_model()


class InviteForm(DynamicFieldsModelForm):
    email = CommaSeparatedEmailField()

    class Meta:
        model = UserInvite
        fields = ('user_type', 'email')
        placeholder = {
            'email': 'Email ID\'s'
        }
        class_map = {
            'email': 'input_group',
            'user_type': 'selectBox'
        }
        hidden_fields = 'user_type',
        non_required_fields = 'email',

    def clean(self):
        attrs = super().clean()
        attrs['emails'] = self.cleaned_data.get('email')
        attrs['email'] = attrs.get('emails')[0]
        return attrs


class RegistrationForm(DynamicFieldsModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'driving_licence', 'password', 'phone', 'image')
        placeholder = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'phone': 'Phone Number',
            'driving_licence': 'Driving Licence'
        }
        class_map = {
            'first_name': 'row',
            'last_name': 'row',
            'email': 'row',
            'password': 'row',
            'phone': 'row',
            'driving_licence': 'row',
            'image': 'row custom-file custom-file-label'
        }
        non_required_fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class DriverListForm(forms.Form):
    drivers = forms.ModelChoiceField(
        queryset=Driver.objects.filter(driver_status=ACTIVE),
        empty_label='Select Driver'
    )


class BundleAssignDriverForm(DynamicFieldsModelForm):
    class Meta:
        model = OrderBundle
        fields = (
            'bundle_id', 'driver'
        )


class BundleAssignStorekeeperForm(DynamicFieldsModelForm):
    class Meta:
        model = OrderBundle
        fields = (
            'bundle_id', 'storekeeper'
        )
