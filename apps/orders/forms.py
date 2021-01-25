from django import forms

from apps.commons.mixins.commons import DynamicFieldsModelForm
from apps.orders.models import OrderBundle, OrderRemark


class OrderProcessForm(forms.ModelForm):
    class Meta:
        model = OrderBundle
        fields = ['order', ]


class OrderBundleForm(DynamicFieldsModelForm):
    class Meta:
        model = OrderBundle
        fields = ['driver']


class OrderRemarkForm(forms.ModelForm):
    class Meta:
        model = OrderRemark
        fields = ['detail']
