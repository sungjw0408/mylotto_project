# lotto/urls.py

from django.urls import path
from . import views

app_name = 'lotto' # 1. 네임스페이스 추가 ('Polls' 앱처럼)
urlpatterns = [
    # 2. 로또 앱의 기본 주소를 lotto_index 뷰와 연결
    path('', views.lotto_index, name='lotto_index'),
    path('winnings/', views.winnings_history, name='winnings_history'),
]