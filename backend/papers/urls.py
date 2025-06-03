from django.urls import path
from .views import PaperListView, PaperDetailView, mark_important

urlpatterns = [
    path('papers/', PaperListView.as_view(), name='paper-list'),
    path('papers/<int:pk>/', PaperDetailView.as_view(), name='paper-detail'),
    path('papers/<int:pk>/important/', mark_important, name='paper-important'),
]
