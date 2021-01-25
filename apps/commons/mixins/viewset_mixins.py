from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class SuccessMessageMixin:
    success_message = {}

    def get_success_message(self, action):
        default_text = f'{action}d'
        if action in ['list', 'destroy']:
            default_text = f'{action}ed'
        return self.success_message.get(
            action,
            f'Successfully {default_text} data.'
        )


class CustomizeCreateModelMixin(SuccessMessageMixin, mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = dict(
            success=True,
            message=self.get_success_message('create'),
            data=serializer.data
        )
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CustomizeUpdateModelMixin(SuccessMessageMixin, mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {
                'success': True,
                'message': self.get_success_message('update'),
                'data': serializer.data
            }
        )


class CustomizeListModelMixin(SuccessMessageMixin, mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'success': True,
                'message': self.get_success_message('list'),
                'data': self.get_paginated_response(serializer.data).data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'message': self.get_success_message('list'),
                'data': serializer.data
            }
        )


class CustomizeRetrieveModelMixin(SuccessMessageMixin, mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                'success': True,
                'message': self.get_success_message('retrieve'),
                'data': serializer.data
            }
        )


class CustomizeDestroyModelMixin(SuccessMessageMixin, mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                'success': True,
                'message': self.get_success_message('destroy')
            },
            status=status.HTTP_204_NO_CONTENT
        )


class CustomizeModelViewSet(CustomizeCreateModelMixin,
                            CustomizeRetrieveModelMixin,
                            CustomizeUpdateModelMixin,
                            CustomizeDestroyModelMixin,
                            CustomizeListModelMixin,
                            GenericViewSet):
    pass


class CreateViewSetMixin(CustomizeCreateModelMixin,
                         GenericViewSet):
    """
    A viewset that provides  `create` action.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class DestroyViewSetMixin(CustomizeDestroyModelMixin,
                          GenericViewSet):
    """
    A viewset that provides  `destory` action.
    """
    pass


class CreateRetrieveUpdateDestroyViewSetMixin(CustomizeCreateModelMixin,
                                              CustomizeRetrieveModelMixin,
                                              CustomizeUpdateModelMixin,
                                              CustomizeDestroyModelMixin,
                                              GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, `update` and
    `destroy` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class CreateRetrieveUpdateViewSetMixin(CustomizeCreateModelMixin,
                                       CustomizeRetrieveModelMixin,
                                       CustomizeUpdateModelMixin,
                                       GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, `update` and
    `destroy` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListCreateUpdateViewSetMixin(CustomizeListModelMixin,
                                   CustomizeCreateModelMixin,
                                   CustomizeUpdateModelMixin,
                                   GenericViewSet):
    """
    A viewset that provides `list`, `create`, and `update` actions
    """
    pass


class ListCreateUpdateDestroyViewSetMixin(CustomizeListModelMixin,
                                          CustomizeCreateModelMixin,
                                          CustomizeUpdateModelMixin,
                                          CustomizeDestroyModelMixin,
                                          GenericViewSet):
    pass


class ListCreateDestroyViewSetMixin(CustomizeListModelMixin,
                                    CustomizeCreateModelMixin,
                                    CustomizeDestroyModelMixin,
                                    GenericViewSet):
    pass


class ListRetrieveUpdateDestroyViewSetMixin(CustomizeListModelMixin,
                                            CustomizeRetrieveModelMixin,
                                            CustomizeUpdateModelMixin,
                                            CustomizeDestroyModelMixin,
                                            GenericViewSet):
    """
    A viewset that provides `list`, `retrieve`, `update` and
    `destroy` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class RetrieveUpdateViewSetMixin(CustomizeRetrieveModelMixin,
                                 CustomizeUpdateModelMixin,
                                 GenericViewSet):
    """
    A viewset that provides `retrieve` and `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListCreateViewSetMixin(CustomizeListModelMixin,
                             CustomizeCreateModelMixin,
                             GenericViewSet):
    """
    A viewset that provides `list` and `create` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListCreateDestroyViewSetMixin(CustomizeListModelMixin,
                                    CustomizeCreateModelMixin,
                                    CustomizeDestroyModelMixin,
                                    GenericViewSet):
    """
    A viewset that provides `list` , `create` and `Destroy` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListRetrieveUpdateViewSetMixin(CustomizeListModelMixin,
                                     CustomizeRetrieveModelMixin,
                                     CustomizeUpdateModelMixin,
                                     GenericViewSet):
    """
    A viewset that provides `list`, `retrieve` and `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class UpdateViewSetMixin(CustomizeListModelMixin,
                         CustomizeUpdateModelMixin,
                         GenericViewSet):
    """
    A viewset that provides `list`, and `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListRetrieveDestroyViewSetMixin(CustomizeListModelMixin,
                                      CustomizeRetrieveModelMixin,
                                      CustomizeDestroyModelMixin,
                                      GenericViewSet):
    """
    A viewset that provides `list`, `retrieve` and `destroy` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListCreateRetrieveViewSetMixin(CustomizeListModelMixin,
                                     CustomizeCreateModelMixin,
                                     CustomizeRetrieveModelMixin,
                                     GenericViewSet):
    """
       A viewset that provides `list`, `create` and `retrieve` actions.

       To use it, override the class and set the `.queryset` and
       `.serializer_class` attributes.
       """
    pass


class ListCreateRetrieveUpdateViewSetMixin(CustomizeListModelMixin,
                                           CustomizeCreateModelMixin,
                                           CustomizeRetrieveModelMixin,
                                           CustomizeUpdateModelMixin,
                                           GenericViewSet):
    """
       A viewset that provides `list`, `create`, `retrieve` and `update` actions

       To use it, override the class and set the `.queryset` and
       `.serializer_class` attributes.
    """


class ListCreateRetrieveDestroyViewSetMixin(CustomizeListModelMixin,
                                            CustomizeCreateModelMixin,
                                            CustomizeRetrieveModelMixin,
                                            CustomizeDestroyModelMixin,
                                            GenericViewSet):
    """
       A viewset that provides `list`, `create`, `retrieve` and `delete` actions

       To use it, override the class and set the `.queryset` and
       `.serializer_class` attributes.
    """


class ListRetrieveViewSetMixin(CustomizeListModelMixin,
                               CustomizeRetrieveModelMixin,
                               GenericViewSet):
    """
    A viewset that provides `list` and `retrieve` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListUpdateViewSetMixin(CustomizeListModelMixin,
                             CustomizeUpdateModelMixin,
                             GenericViewSet):
    """
    A viewset that provides `list` and `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class RetrieveViewSetMixin(CustomizeRetrieveModelMixin,
                           GenericViewSet):
    """
    A viewset that provides `retrieve` action.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListViewSetMixin(CustomizeListModelMixin,
                       GenericViewSet):
    """
           A viewset that provides `list` action

           To use it, override the class and set the `.queryset` and
           `.serializer_class` attributes.
        """
    pass


class CreateUpdateViewSetMixin(CustomizeCreateModelMixin,
                               CustomizeUpdateModelMixin,
                               GenericViewSet):
    pass


class CreateUpdateDeleteViewSetMixin(CustomizeCreateModelMixin,
                                     CustomizeUpdateModelMixin,
                                     CustomizeDestroyModelMixin,
                                     GenericViewSet):
    pass


class CreateDeleteViewSetMixin(CustomizeCreateModelMixin,
                               CustomizeDestroyModelMixin,
                               GenericViewSet):
    pass
