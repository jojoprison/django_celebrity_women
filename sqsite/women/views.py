from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse('Страница приложения women.')


# имя параметра совпадает с его именем в маппинге
def categories(request, catid):
    if request.POST:
        print(request.POST)

    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{catid}</p>')


def archive(request, year):
    if int(year) > 2020:
        # автоматически перенаправляется на метод pageNotFound
        # raise Http404()
        # чтоб не хардкодить явный url адрес линки указывают его имя вместо пути
        return redirect('home', permanent=True)

    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
