from django import forms

from apps.commons.mixins.commons import DynamicFieldsModelForm
from apps.warehouse.models import Warehouse, Product


class WareHouseForm(DynamicFieldsModelForm):
    aisle_map = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Warehouse
        fields = [
            'name', 'description', 'email', 'contact', 'address', 'longitude',
            'latitude', 'location_range_type', 'location_range', 'aisle_map'
        ]
        non_required_fields = ['aisle_map']
        placeholder = {
            'name': 'Warehouse Name',
            'description': 'Warehouse Description',
            'email': 'Warehouse Email ID',
            'contact': 'Warehouse Contact Number',
            'address': 'Warehouse Address',
            'location_range': 'Enter Data'
        }
        hidden_fields = ['longitude', 'latitude', 'aisle_map']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_range = self.fields['location_range']
        location_range_type = self.fields['location_range_type']
        description = self.fields['description']
        address = self.fields['address']
        aisle_map = self.fields['aisle_map']

        location_range.widget.attrs.update({
            'class': 'search_input'
        })
        location_range_type.widget.attrs.update({
            'class': 'dd'
        })
        description.widget.attrs.update({'rows': 4})
        address.widget.attrs.update({'rows': 6})
        aisle_map.widget.attrs.update({
            'class': 'file-upload',
            'onchange': 'readURL(this)',
        })


class ProductForm(DynamicFieldsModelForm):
    class Meta:
        model = Product
        exclude = 'parent_product', 'product_structure', 'product_type',
        readonly_fields = 'slug',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ignore_fields = ['is_discountable', 'is_active']
        for key, field in self.fields.items():
            if key not in ignore_fields:
                field.widget.attrs.update({
                    'class': 'form-control'
                })
            if key == 'description':
                field.widget.attrs.update({
                    'rows': 3
                })
