"""
VentureLens AI - Dashboard URLs
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('<uuid:pk>/', views.ResultsDashboardView.as_view(), name='results'),
    path('<uuid:pk>/processing/', views.ProcessingView.as_view(), name='processing'),
    path('<uuid:pk>/delete/', views.DeleteAnalysisView.as_view(), name='delete'),
    path('history/', views.HistoryView.as_view(), name='history'),
]