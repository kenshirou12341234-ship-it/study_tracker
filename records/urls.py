from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.RecordListView.as_view(), name='list'),
    path('create/', views.RecordCreateView.as_view(), name='create'),
    path('<int:pk>/', views.RecordDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.RecordUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.RecordDeleteView.as_view(), name='delete'),
]