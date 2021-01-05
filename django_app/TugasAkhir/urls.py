from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sentiment', views.sen_default, name='sentiment'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('map',views.map, name='map'),
    path('inputan',views.inputan_sentimen, name='inputan'),
]