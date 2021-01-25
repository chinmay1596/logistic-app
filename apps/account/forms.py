from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from apps.account.models import Address
from apps.commons.mixins.commons import DynamicFieldsModelForm

UserModel = get_user_model()


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country_code', 'country_name', 'state',
                  'city_name', 'street', 'locality_name']


# Sign Up Form
class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'First Name...'}), max_length=200,
                                 required=True, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Last Name...'}), max_length=200,
                                required=True, )
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Email address..."}), required=True,
                            max_length=75)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password..."}),
                               validators=[validate_password])

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'password']


class ProfileForm(DynamicFieldsModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'phone', 'email', 'image']
        # readonly_fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        placeholder = {
            'first_name': 'Enter Your First Name',
            'last_name': 'Enter Your Last Name',
            'email': 'Enter Your Email ID',
            'phone': 'Enter Your Phone Number',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
