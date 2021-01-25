from django import forms
from django.urls import reverse_lazy

from apps.analytics.contants import REPORT_TYPE_CHOICES, REPORT_TYPE_DISPLAY_CHOICES
from apps.employee.models import Driver

FILTER_CHOICES = tuple(
    zip(
        map(
            lambda x: reverse_lazy(
                'analytics:common-analytics-list',
                kwargs={'report_type': x}
            ),
            REPORT_TYPE_CHOICES
        ),
        REPORT_TYPE_DISPLAY_CHOICES
    )
)


class AnalyticsFilterForm(forms.Form):
    report_type = forms.ChoiceField(
        choices=FILTER_CHOICES,
        widget=forms.Select(attrs={'class': 'select'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'datepicker', 'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off'}),
        required=False)
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'end-datepicker', 'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off'}),
        required=False)
