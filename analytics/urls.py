from django.urls import path
from analytics.views import ucl_dashboard_view

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', ucl_dashboard_view, name='ucl_dashboard'),
]