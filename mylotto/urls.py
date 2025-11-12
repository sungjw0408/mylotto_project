# mylotto/urls.py

from django.contrib import admin
from django.urls import path, include  # 1. include를 가져옵니다.
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. 'lotto/' 주소는 'lotto.urls'가 담당
    path('lotto/', include('lotto.urls')), 

    # 3. 'accounts/' 주소는 'users.urls'가 담당
    path('accounts/', include('users.urls')),

    # 4. Django 기본 로그인/로그아웃 URL 포함
    path('accounts/', include('django.contrib.auth.urls')), 
]