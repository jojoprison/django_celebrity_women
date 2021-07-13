from django.urls import path, re_path

from .views import *

urlpatterns = [
    # имя для маршрута, чтобы юзать во вьюхах
    path('', index, name='home'),
    path('cats/<int:catid>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
