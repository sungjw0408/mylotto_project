from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 'lotto/' 주소 'lotto.urls' 담당
    path('lotto/', include('lotto.urls')), 

    # 'accounts/' 주소'users.urls' 담당
    path('accounts/', include('users.urls')),

    # Django 기본 로그인/로그아웃 URL
    path('accounts/', include('django.contrib.auth.urls')), 
]