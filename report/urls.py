from django.urls import path
from .views import daily_report, weekly_report, monthly_report, yearly_report, report_view, export_report_doc



urlpatterns = [
    path('report/', report_view, name='report'),
    path('report/daily/', daily_report, name='daily_report'),
    path('report/weekly/', weekly_report, name='weekly_report'),
    path('report/monthly/', monthly_report, name='monthly_report'),
    path('report/yearly/', yearly_report, name='yearly_report'),
    path('export-report/<str:report_type>/', export_report_doc, name='export_report'),
]

