from import_export import resources
from apps.warehouse.models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ('warehouse',)