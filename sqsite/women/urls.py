from django.urls import path, re_path

from .views import *

urlpatterns = [
    # имя для маршрута, чтобы юзать во вьюхах
    path('', index, name='home'),
    path('about/', about, name='about'),
]
