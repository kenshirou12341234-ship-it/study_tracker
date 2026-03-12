from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from records.views import register  # ← 追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register, name='register'),  # ← 追加
    path('accounts/', include('django.contrib.auth.urls')),  # ← ここに追加！
    path('records/', include('records.urls')),
    path('', RedirectView.as_view(url='/records/', permanent=False)),
]
