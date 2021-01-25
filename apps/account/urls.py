from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from apps.account.views import SignUpView, activate, CustomPasswordChangeView,UserDetailView,UserUpdateView
from django.contrib.auth.views import (LoginView, LogoutView,PasswordResetDoneView,PasswordResetConfirmView,
PasswordResetCompleteView,PasswordResetView)

app_name = 'account'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', UserUpdateView.as_view(), name='profile_update'),
    path('', LoginView.as_view(), {'template_name': 'registration/login.html'}, name='login'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('account:password_reset_done')),
                                                    {'template_name': 'registration/password_reset_form.html'},
                                                    name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
                                   name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete')),
                                                                    name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('firebase-messaging-sw.js', TemplateView.as_view(template_name='notification/firebase-messaging-sw.js',
                                                          content_type="application/x-javascript"))
    ]
