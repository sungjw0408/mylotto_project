from django.urls import path
from . import views

app_name = 'lotto' 
urlpatterns = [
    path('', views.lotto_index, name='lotto_index'),
    path('winnings/', views.winnings_history, name='winnings_history'),
]