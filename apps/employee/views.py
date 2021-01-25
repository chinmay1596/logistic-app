from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Case, When, Value, CharField, Exists, OuterRef
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.commons.mixins.commons import CustomCreateView, LoginAndPermissionMixin
from apps.commons.mixins.commons import (
    CustomListView
)
from apps.employee.forms import InviteForm, RegistrationForm, BundleAssignDriverForm, BundleAssignStorekeeperForm
from apps.orders.constants import STORE_KEEPER_ASSIGNED, DELIVERED
from utils import emailing
from .constants import STORE_KEEPER, DRIVER, COMPLETE, OFF_DUTY, ASSIGNED
from .models import (
    UserInvite, Driver, StoreKeeper
)
from ..commons.mixins.viewset_mixins import ListViewSetMixin
from ..orders.models import OrderBundle, OrderItem

UserModel = get_user_model()
ANNOTATE_FILTER = dict(
    shift_status_text=Case(
        When(
            shift_status=OFF_DUTY,
            then=Value('start')
        ),
        When(
            shift_status=COMPLETE,
            then=Value('start')
        ),
        default=Value('end'),
        output_field=CharField()
    ),
    shift_status_color=Case(
        When(
            shift_status=COMPLETE,
            then=Value('info')
        ),
        When(
            shift_status=OFF_DUTY,
            then=Value('danger')
        ),
        default=Value('success active'),
        output_field=CharField()
    )
)


class EmployeeInvitationView(CustomCreateView):
    model = UserInvite
    form_class = InviteForm
    http_method_names = ['post', 'put', 'patch',
                         'delete', 'head', 'options', 'trace']
    success_message = 'Invitation sent successfully.'

    def get_html_message(self, email):
        company = settings.COMPANY_NAME
        uuid = urlsafe_base64_encode(force_bytes(email))
        url = f'{settings.BACKEND_BASE_URL}{reverse_lazy("employee:register", kwargs={"uidb64": uuid})}'
        return f'''
            <p>
                Hello There, <br><br>
                
                I am delighted to invite you on behalf of <strong>{company}</strong> to become a member of our 
                company as {self.kwargs.get('employee_type')}.<br><br>
                
                Now, the important details: <br>
                <a href='{url}'> Click here to sign up today and know more about <strong>{company}</strong> </a>. <br><br>
                
                Thank you for your consideration, We are looking forward to hearing from you and hope to see you 
                associated with our company.<br><br>
                
                Best regards
            </p>
        '''

    def perform_save(self, form):
        emails = form.cleaned_data.get('emails')
        user_type = form.cleaned_data.get('user_type')

        message_subject = "Invitation to join logistics Platform"

        new_user_invite = []
        for email in emails:
            message = self.get_html_message(email)
            emailing.EmailThread(
                subject=message_subject,
                html_content=message,
                context=settings.EMAIL_FROM,
                recipient_list=[email]
            ).start()
            new_user_invite.append(
                UserInvite(user_type=user_type, email=email)
            )
        if new_user_invite:
            UserInvite.objects.bulk_create(new_user_invite)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Unable to send invitation due to invalid email\'s.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('employee:list-employee', kwargs={'employee_type': self.kwargs.get('employee_type')})


class EmployeeRegistrationView(CustomCreateView):
    model = UserInvite
    template_name = 'employee/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('employee:activated')
    associated_email = ''
    user_invite = None

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'email': self.associated_email
        })
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.validate_url()
        if self.user_invite.user:
            self.object = self.user_invite
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def validate_url(self):
        associated_email = force_text(
            urlsafe_base64_decode(self.kwargs.get('uidb64')))
        try:
            self.user_invite = self.get_queryset().get(email=associated_email)
            self.associated_email = associated_email
        except UserInvite.DoesNotExist:
            raise Http404(
                f'No invitation sent to user with email {associated_email}')

    def create_user(self, data):
        password = data.pop('password')
        user_invite = self.user_invite

        user = UserModel.objects.create(
            user_type=user_invite.user_type,
            is_verified=True,
            is_active=True,
            **data
        )
        user.set_password(password)
        user.groups.add(Group.objects.get(name=user_invite.user_type))
        user.save()

        user_invite.user = user
        user_invite.save()

        if user_invite.user_type == 'Driver':
            _ = Driver.objects.create(
                user=user, driving_license=data.get('driving_license'))
        elif user_invite.user_type == 'Store Keeper':
            _ = StoreKeeper.objects.create(user=user)
        messages.success(self.request, "Registration successful.")
        return user_invite

    def form_valid(self, form):
        self.object = self.create_user(form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())


class EmployeeListView(CustomListView):
    template_name = 'employee/employee_base.html'

    def get_base_queryset(self):
        if self.kwargs.get('employee_type') == 'driver':
            return Driver.objects.all()
        return StoreKeeper.objects.all()

    def get_annotate_filter(self):
        if self.kwargs.get('employee_type') == 'driver':
            return {'driver': OuterRef('id')}
        return {'storekeeper': OuterRef('id')}

    def get_queryset(self):
        queryset = self.get_base_queryset()
        queryset = queryset.annotate(
            # assigned=None,
            **ANNOTATE_FILTER,
            active_bundle=Exists(
                OrderBundle.objects.filter(
                    **self.get_annotate_filter()
                ).exclude(status=DELIVERED)
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        display_type = self.kwargs.get('display_type')
        employee_type = DRIVER if self.kwargs.get(
            'employee_type') == 'driver' else STORE_KEEPER
        if not display_type:
            context['form'] = InviteForm(
                initial={
                    'user_type': employee_type
                }
            )
        context['employee_type'] = self.kwargs.get('employee_type')
        context['employee_type_text'] = employee_type
        context['display_type'] = display_type
        if self.request.GET.get('bundleid'):
            context['bundle_id'] = self.request.GET.get('bundleid')
        return context


class EmployeeActivityView(CustomListView):
    employee = None
    template_name = 'employee/employee_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.employee = self.get_employee_objects()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('activity_type') == 'orders':
            return OrderItem.objects.filter(
                **{f'order__bundle__{self.kwargs.get("employee_type")}': self.employee}
            )
        return OrderItem.objects.filter(
            **{f'order__bundle__{self.kwargs.get("employee_type")}': self.employee}
        )

    def get_base_queryset(self):
        if self.kwargs.get('employee_type') == 'driver':
            queryset = Driver.objects.all()
        else:
            queryset = StoreKeeper.objects.all()

        return queryset.annotate(**ANNOTATE_FILTER)

    def get_employee_objects(self):
        try:
            return self.get_base_queryset().get(id=self.kwargs.get('pk'))
        except:
            raise Http404('No data found.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_type'] = self.kwargs.get('employee_type')
        context['activity_type'] = self.kwargs.get('activity_type')
        context['object'] = self.employee
        return context


class AssignEmployeeShift(ListViewSetMixin):
    serializer_class = type('DummySerializer', (serializers.Serializer,), {})
    permission_classes = []

    def get_queryset(self):
        if self.kwargs.get('employee_type') == 'driver':
            return Driver.objects.all()
        return StoreKeeper.objects.all()

    def list(self, request, *args, **kwargs):
        status_map = {
            'end': COMPLETE,
            'start': ASSIGNED,
            'off-duty': OFF_DUTY
        }
        color_map = {
            COMPLETE: 'text-info',
            ASSIGNED: 'text-success',
            OFF_DUTY: 'text-danger'
        }
        shift_status = status_map.get(self.kwargs.get('shift_status'))
        employee_id = self.kwargs.get('employee_id')
        instance = get_object_or_404(self.get_queryset(), id=employee_id)
        instance.shift_status = shift_status
        instance.save()
        new_shift_status = 'end' if shift_status == ASSIGNED else 'start'
        return Response(
            {
                'shift_status': shift_status,
                'shift_status_text': f'{new_shift_status.title()} Shift',
                'shift_status_url': reverse_lazy(
                    'employee_api:assign-shift-list',
                    kwargs={
                        'employee_type': self.kwargs.get('employee_type'),
                        'employee_id': instance.id,
                        'shift_status': new_shift_status
                    }
                ),
                'shift_status_text_color': color_map.get(shift_status)
            },
            status=status.HTTP_200_OK
        )


class AssignEmployeeBundle(LoginAndPermissionMixin, FormView):

    def get_success_url(self):
        return reverse_lazy(
            'employee:list-employee',
            kwargs={
                'employee_type': self.kwargs.get('employee_type')
            }
        )

    def get_form_class(self):
        if self.kwargs.get('employee_type') == 'driver':
            return BundleAssignDriverForm
        return BundleAssignStorekeeperForm

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        bundle_id = cleaned_data.get('bundle_id')
        employee_type = self.kwargs.get('employee_type')
        employee = cleaned_data.get(employee_type)
        bundle = get_object_or_404(
            OrderBundle,
            id=bundle_id
        )
        setattr(bundle, employee_type, employee)
        bundle.save()
        return super().form_valid(form)


def assignstorekeeper(request, storekeeper_id, bundle_id):
    storekeepers = StoreKeeper.objects.filter(user__id=storekeeper_id).first()
    assign = OrderBundle.objects.filter(bundle_id=bundle_id).update(store_keeper=storekeepers,
                                                                    status=STORE_KEEPER_ASSIGNED)
    return redirect('employee:storeKeeper_order_activity', pk=storekeeper_id)
