from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from utils import emailing
from .forms import SignUpForm, ProfileForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from utils.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.messages.views import SuccessMessageMixin

from ..commons.mixins.commons import CustomDetailView, CustomUpdateView

UserModel = get_user_model()


# Sign Up View
class SignUpView(SuccessMessageMixin, View):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserModel.objects.create(first_name=first_name, last_name=last_name, email=email, password=password,
                                            user_type='Merchant')
            user.set_password(password)
            user.groups.add(Group.objects.get(name='Merchant'))
            user.save()
            messages.success(self.request, "Signup successful. Please check your email.")
            current_site = get_current_site(request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            mail_subject = 'Activate your Halo Logistics account.'
            message = render_to_string('registration/verification.html', context)
            # email_plaintext_message = render_to_string('authentication/verification.txt', context)
            emailing.EmailThread(mail_subject, message, context, [email, ]).start()
            return redirect('account:signup')
        return render(request, self.template_name, {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        return render(request, "registration/activation_valid.html")
    else:
        return HttpResponse('Activation link is invalid!')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/pwd_change.html'
    success_url = reverse_lazy('account:change_password')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)


class UserDetailView(CustomDetailView):
    template_name = 'profile/profile.html'
    queryset = UserModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == self.request.user.id:
            user_obj = UserModel.objects.get(id=self.kwargs['pk'])
            context['user_obj'] = user_obj
            return context
        else:
            raise PermissionDenied


class UserUpdateView(CustomUpdateView):
    form_class = ProfileForm
    model = UserModel
    template_name = 'profile/profile_update.html'
    success_message = "Profile Updated Successfully."

    def get_success_url(self):
        return reverse_lazy('account:profile', kwargs={'pk': self.get_object().id})

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password-reset-done.html'