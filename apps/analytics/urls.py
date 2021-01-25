from django.urls import path, re_path

from apps.analytics.views import CommonAnalyticsView, CommonExportAnalyticsView
from . import views
from .contants import REPORT_TYPE_CHOICES

app_name = 'analytics'

urlpatterns = [
    re_path(
        r'(?P<report_type>({name}))/export'.format(name="|".join(REPORT_TYPE_CHOICES)),
        CommonExportAnalyticsView.as_view(),
        name='common-analytics-export'),
    re_path(
        r'(?P<report_type>({name}))'.format(name="|".join(REPORT_TYPE_CHOICES)),
        CommonAnalyticsView.as_view(),
        name='common-analytics-list'),

]
