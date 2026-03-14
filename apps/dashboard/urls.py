from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('<uuid:pk>/', views.ResultsDashboardView.as_view(), name='results'),
    path('<uuid:pk>/processing/', views.ProcessingView.as_view(), name='processing'),
    path('<uuid:pk>/delete/', views.DeleteAnalysisView.as_view(), name='delete'),
    path('<uuid:pk>/share/', views.GenerateShareLinkView.as_view(), name='share'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('shared/<uuid:token>/', views.SharedResultsView.as_view(), name='shared'),
]