from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.IdeaInputView.as_view(), name='input'),
    path('<uuid:pk>/processing/', views.AnalysisProcessingView.as_view(), name='processing'),
    path('<uuid:pk>/status/', views.AnalysisStatusView.as_view(), name='status'),
    path('<uuid:pk>/trends/', views.TrendsTimeframeView.as_view(), name='trends'),
    path('<uuid:pk>/feedback/', views.FeedbackView.as_view(), name='feedback'),
]