from django.urls import path
from . import views

urlpatterns = [
    # ダッシュボード
    path('', views.dashboard, name='dashboard'),
    
    # 学習記録
    path('records/', views.record_list, name='record_list'),
    path('records/create/', views.record_create, name='record_create'),
    path('records/<int:pk>/edit/', views.record_update, name='record_update'),
    path('records/<int:pk>/delete/', views.record_delete, name='record_delete'),
    
    # 学習項目
    path('certifications/', views.certification_list, name='certification_list'),
    path('certifications/create/', views.certification_create, name='certification_create'),
    path('certifications/<int:pk>/edit/', views.certification_update, name='certification_update'),
    path('certifications/<int:pk>/delete/', views.certification_delete, name='certification_delete'),
]