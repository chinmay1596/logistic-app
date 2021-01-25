from fcm_django.models import FCMDevice
from django.contrib.auth import authenticate
from apps.notification.models import Notification, SerializeNotification
from django.contrib.auth import get_user_model
from apps.commons.mixins.commons import (CustomAjaxListView, CustomAjaxUpdateView, CustomAjaxCreateView)
from apps.notification.forms import (CreateFCMDeviceForm, ReadNotificationUpdateForm)
from django.http import JsonResponse

User = get_user_model()


class CreateTokenView(CustomAjaxCreateView):
    model = FCMDevice
    form_class = CreateFCMDeviceForm
    user_object = None

    def form_valid(self, form):
        self.perform_authenticate()
        if self.user_object:
            form.instance.user = self.user_object
            form.instance.name = self.user_object.full_name
            form.save()
        return JsonResponse({'success': True}, status=200)

    def perform_authenticate(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        self.user_object = authenticate(email=username, password=password)


class NotificationListView(CustomAjaxListView):
    allow_empty_first_page = False
    model = SerializeNotification
    paginated_by = 3
    queryset_object = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs['pk']
        self.queryset_object = queryset.filter(user=user_id).order_by('-id')
        return self.queryset_object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'notification_count': self.queryset_object.filter(read=False).count(),
        })
        return context


class MarkReadNotificationView(CustomAjaxUpdateView):
    model = Notification
    form_class = ReadNotificationUpdateForm
    notification_object = None

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        self.perform_response(form)
        return JsonResponse({'notification_count': self.notification_object}, status=200)

    def perform_response(self, form):
        queryset = super().get_queryset()
        user = form.instance.user
        self.notification_object = queryset.filter(read=False, user=user).count()
