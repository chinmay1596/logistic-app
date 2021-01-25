from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.commons.utils.custom_pagination import CustomPagination
from apps.orders.api.serializers import (CreateOrderSerializer, OrderItemSerializer, OrderDetailSerializer,
                                         OrderUpdateSerializer, OrderListSerializer, BundleSerializer,
                                         CancelOrderSerializer, ReturnOrderSerializer)
from apps.orders.filters import OrderFilter
from apps.orders.models import Order, OrderItem, OrderBundle
from apps.warehouse.models import WarehouseProduct, Product
from apps.orders.constants import CANCELLED, RETURN
from apps.commons.mixins.viewset_mixins import (RetrieveViewSetMixin, UpdateViewSetMixin)
from utils.notification import send_notification


class OrderCreateAPIView(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = OrderFilter
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.all().order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                instance = serializer.save(uuid=serializer.validated_data.get('uuid'))
                order_item_serializer = OrderItemSerializer(data=request.data)
                order_item_serializer.is_valid(raise_exception=True)
                products = order_item_serializer.validated_data['product']
                for product in products:
                    try:
                        warehouse_product = Product.objects.get(id=product["id"],
                                                                warehouse=serializer.validated_data['warehouse'],
                                                                units__gt=0)
                    except Product.DoesNotExist:
                        raise NotFound({'success': False, 'message': 'Product does not exist in our database '
                                                                     'or is out of the stock at the moment.'})
                    OrderItem.objects.create(order=Order.objects.get(id=instance.id),
                                             product=warehouse_product,
                                             units=product["units"])
                    warehouse_product.units -= product["units"]
                    print(warehouse_product.units)
                    warehouse_product.save()

                return Response({'data': serializer.data, 'success': True, 'message': 'Order created successfully'},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': 'Order Creation Failed.'},
                            status=status.HTTP_400_BAD_REQUEST)


class OrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = OrderDetailSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        try:
            order_obj = Order.objects.get(id=self.kwargs['pk'])
            order_data = self.serializer_class(order_obj).data
            return Response({'success': True, 'data': order_data, 'message': 'Order fetched successfully'},
                            status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise NotFound({'success': False, 'message': 'Order with the provided id does not exist in our database.'})

    def update(self, request, *args, **kwargs):
        try:
            order_obj = Order.objects.get(id=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise NotFound({'success': False, 'message': 'Order with the provided id does not exist in our database.'})
        serializer = OrderUpdateSerializer(order_obj, data=request.data, partial=True)
        item_serializer = OrderItemSerializer(data=request.data, partial=True)
        if item_serializer.is_valid(raise_exception=True):
            products = item_serializer.validated_data.get('product')
            if products:
                for product in products:
                    try:
                        warehouse_product = Product.objects.get(id=product["id"], units__gt=0)
                    except Product.DoesNotExist:
                        raise NotFound({'success': False,
                                        'message': 'Product does not exist in our database or'
                                                   ' is out of the stock at the moment'})
                    item, created = OrderItem.objects.get_or_create(order=order_obj, product=warehouse_product,
                                                                    defaults={'units': product['units']})
                    if product['ordered']:
                        if item:
                            warehouse_product.units += item.units
                            item.units = product['units']
                            item.save()
                    else:
                        item.delete()

                    warehouse_product.units -= product["units"]
                    warehouse_product.save()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': 'Order updated successfully', 'data': serializer.data},
                            status=status.HTTP_200_OK)


class BundleRetrieveAPIView(RetrieveViewSetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = BundleSerializer
    queryset = OrderBundle.objects.all()


class CancelOrderAPIView(UpdateViewSetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = CancelOrderSerializer
    queryset = Order.objects.filter(order_status=CANCELLED)

    def update(self, request, *args, **kwargs):
        order_obj = Order.objects.get(id=self.kwargs['pk'])
        order_obj.order_status = CANCELLED
        order_obj.reason_for_cancellation = request.data['reason_for_cancellation']
        order_obj.save()
        message = f"order #{order_obj.uuid} cancelled"
        click_action = f"/orders/detail/{order_obj.id}/"
        send_notification(user_id=order_obj.merchant.id, title='Order Cancelled',
                          message=message,
                          click_action=click_action, data=None)
        return Response({'success': True, 'message': 'Order Cancelled successfully'})


class ReturnOrderAPIView(UpdateViewSetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReturnOrderSerializer
    queryset = Order.objects.filter(order_status=RETURN)

    def update(self, request, *args, **kwargs):
        order_obj = Order.objects.get(id=self.kwargs['pk'])
        order_obj.order_status = RETURN
        order_obj.save()
        message = f"order #{order_obj.uuid} returns"
        click_action = f"/orders/detail/{order_obj.id}/"
        send_notification(user_id=order_obj.merchant.id, title="Order Return", message=message,
                          click_action=click_action, data=None)
        return Response({'success': True, 'message': 'Order return successfully'})
