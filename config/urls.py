from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from records.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # アカウント関連
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # ← 修正
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 学習記録関連
    path('records/', include('records.urls')),
    
    # ルート URL → 学習記録一覧にリダイレクト
    path('', RedirectView.as_view(url='/records/', permanent=False)),
]