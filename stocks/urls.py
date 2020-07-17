from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/<Portfolios_id>', views.get, name='get'),
    path('update/', views.update, name = 'update'),
    path('reset/', views.reset, name='reset'),
    path('history/', views.history, name='history'),
    path('symbol/', views.symbol, name='symbol'),
]