from django.contrib import messages
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.utils.functional import cached_property
from apps.commons.mixins.commons import CustomAjaxCreateView, CustomDeleteView, CustomAjaxListView, CustomUpdateView, \
    CustomAjaxUpdateView
from apps.warehouse.forms import ProductForm
from django.core.serializers import serialize
from apps.warehouse.models import Product, Warehouse, WarehouseProduct, SerializeWarehouseProduct, Shelf, Bay
from django.views.generic import View


class BaseWarehouseMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if self.warehouse:
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({'detail': 'Warehouse not found.'}, status=404)

    @cached_property
    def warehouse(self):
        return Warehouse.objects.filter(id=self.kwargs.get('warehouse_id')).first()


class ProductCreateView(BaseWarehouseMixin, CustomAjaxCreateView):
    form_class = ProductForm
    model = Product

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        title = cleaned_data.pop('title')
        units = cleaned_data.get('units')
        product, created = Product.objects.get_or_create(
            title=title,
            defaults=cleaned_data
        )

        if self.warehouse.products.filter(product=product).exists():
            return JsonResponse({'detail': 'Product already exists.'}, status=400)

        response = SerializeWarehouseProduct.objects.create(
            product=product, warehouse=self.warehouse, units=units)
        if not created:
            product.units = product.units + units
            product.save()

        self.object = product
        return JsonResponse(response.to_dict(), status=200)


class ProductDeleteView(CustomDeleteView):
    model = WarehouseProduct

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'detail': 'Successfully deleted content.'}, status=203)

    def get_object(self, queryset=None):
        try:
            super().get_object(queryset)
        except (Http404, AttributeError):
            return JsonResponse({'detail': 'No data found.'}, status=404)

    def get_queryset(self):
        return super().get_queryset().filter(warehouse_id=self.kwargs.get('warehouse_id'))


class ProductListView(CustomAjaxListView):
    queryset = SerializeWarehouseProduct.objects.all()
    paginate_by = 5
    allow_empty_first_page = False

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(warehouse=self.kwargs.get('warehouse_id')).select_related('warehouse', 'product')


class ProductQuantityUpdateView(View):

    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        WarehouseProduct.objects.filter(id=product_id).update(
            units=self.request.POST.get('quantity'))
        warehouse_data = WarehouseProduct.objects.get(id=product_id)
        messages.success(request, 'Quantity updated successfully.')
        return redirect('/warehouse/detail/' + str(warehouse_data.warehouse.id) + '/')


class LocationUpdateView(View):
    def post(self, request, *args, **kwargs):
        warehouse_data = WarehouseProduct.objects.get(
            id=self.request.POST.get('product_id'))
        Shelf.objects.filter(id=warehouse_data.location.id).update(
            abbreviation=self.request.POST.get('shelf'))
        Bay.objects.filter(id=warehouse_data.location.bay.id).update(
            abbreviation=self.request.POST.get('bay'))
        messages.success(request, 'Position updated successfully.')
        return redirect('/warehouse/detail/' + str(warehouse_data.warehouse.id) + '/')
