# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 'signup/' 주소로 접속하면 signup 뷰를 실행
    path('signup/', views.signup, name='signup'),
]