"""sqsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from sqsite import settings
from women.views import *
from django.urls import path, include

from django.views.static import serve as mediaserve
# from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # маппинг для модуля с капчей из доков
    path('captcha/', include('captcha.urls')),
    # данный префикс всегда будет добавляться к линкам
    path('', include('women.urls')),
]

if settings.DEBUG:
    # вне дебага не будет работать
    import debug_toolbar

    # для django_debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    pass
    # костыль, чтобы на хосте статик файлы корректно брались из папок
    # urlpatterns += [
        # url(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
        #     mediaserve, {'document_root': settings.MEDIA_ROOT}),
        # url(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*$',
        #     mediaserve, {'document_root': settings.STATIC_ROOT}),
    # ]

# есть handler500, handler400  и тд
handler404 = pageNotFound
