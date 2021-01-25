from django.contrib.auth.decorators import permission_required


class CheckPermissionCreateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.add_%s' % (self.model._meta.app_label, self.model._meta.model_name),
                             raise_exception=True)
        def wrapper(request, *args, **kwargs):
            return super(CheckPermissionCreateMixin, self).dispatch(request, *args, **kwargs)

        return wrapper(request, *args, **kwargs)


class CheckPermissionListMixin(object):
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.view_%s' % (self.model._meta.app_label, self.model._meta.model_name),
                             raise_exception=True)
        def wrapper(request, *args, **kwargs):
            return super(CheckPermissionListMixin, self).dispatch(request, *args, **kwargs)

        return wrapper(request, *args, **kwargs)


class CheckPermissionUpdateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.change_%s' % (self.model._meta.app_label, self.model._meta.model_name),
                             raise_exception=True)
        def wrapper(request, *args, **kwargs):
            return super(CheckPermissionUpdateMixin, self).dispatch(request, *args, **kwargs)

        return wrapper(request, *args, **kwargs)


class CheckPermissionDeleteMixin(object):
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.delete_%s' % (self.model._meta.app_label, self.model._meta.model_name),
                             raise_exception=True)
        def wrapper(request, *args, **kwargs):
            return super(CheckPermissionDeleteMixin, self).dispatch(request, *args, **kwargs)

        return wrapper(request, *args, **kwargs)


class CheckPermissionDetailMixin(object):
    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.detail_%s' % (self.model._meta.app_label, self.model._meta.model_name),
                             raise_exception=True)
        def wrapper(request, *args, **kwargs):
            return super(CheckPermissionDetailMixin, self).dispatch(request, *args, **kwargs)

        return wrapper(request, *args, **kwargs)
