from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'records'  # ← この行を追加

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
    
    # 認証
    path('login/', auth_views.LoginView.as_view(template_name='records/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]