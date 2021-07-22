from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# кастомный CBV (classes-based view)
# первый наследуемый класс первым и обрабатывается, то есть повторяющиеся
# аттрибуты берутся из первого родительского класса,
# поэтому миксины лучшез записывать в первую очередь
class WomenHome(DataMixin, ListView):
    model = Women
    # по дефолту будет women/women_list.html
    template_name = 'women/index.html'
    # по дефолту будет object_list
    context_object_name = 'posts'
    # передает только статические незименяемые значения (если без get_context_data)
    # extra_context = {'title': 'Главная страница'}
    # пагинация уже есть в ListView, нужно лишь задать кол-во элементов на странице
    # ListView АВТОМАТИЧЕСКИ передает в темплейт объекты paginator и page_obj
    # paginate_by = 3

    # формирует и статический и динамический контекст, передаваемый в шаблон
    def get_context_data(self, *, object_list=None, **kwargs):
        # получаем контекст, сформированный на основе базового класса ListView
        context = super().get_context_data(**kwargs)

        # заносим в контекст новое значение с тайтлом, остальное берем из миксины
        c_def = self.get_user_context(title='Главная страница')

        # объединяем 2 словаря в общий контекст
        # return dict(list(context.items()) + list(c_def.items()))
        # до 3.9:
        # return {**context, **c_def}
        # после 3.9:
        return context | c_def

    # что именно выбирать из модели и передавать на вьюху
    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# способ отображения представления через функцию
# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)

def about(request):
    # пример пагинации внутри функций представления:
    contact_list = Women.objects.all()

    # будет отображаться 3 элемента списка на каждой странице
    paginator = Paginator(contact_list, 3)

    # получаем номер текущей страницы из запроса по параметру page из GET запроса
    page_number = request.GET.get('page')
    # получаем список элементов текущей страницы по ее номеру
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте',
                                                'page_obj': page_obj})


# вместо нее класс представления для отображения формы (createview)
# def addpage(request):
#
#     # если форма уже отправлялась - чтобы не терялись введенные данные
#     if request.method == 'POST':
#         # создаем форму, передавая уже существующие параметры из POST запроса
#         # FILES - список, файлов, переданные на серв из формы
#         form = AddPostForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             # данные из переданной формы
#             # print(form.cleaned_data)
#
#             # так мы изначально сохраняли данные из формы в бд
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#
#             # когда форма связана с моделью, можно вот так
#             # все данные, переданные от формы, будут автоматически занесены
#             # в таблицы бд связанной модели
#             form.save()
#
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'form': form , 'menu': menu,
#                                                   'title': 'Добавление статьи'})

# описание структуры наследования выше
# LoginRequiredMixin - миксина выдает 404 для неавторизованных пользователей
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    # аттрибут указывает на класс формы, который будет подключаться к классу вида
    form_class = AddPostForm
    # подключаем шаблон для формы
    template_name = 'women/addpage.html'
    # куда переходим в случае успешной отправки формы
    # reverse - пытается сразу построить маршрут в момент создания объекта
    # reverse_lazy - выполняет построение маршрута только в момент, когда он понадобится
    success_url = reverse_lazy('home')
    # указывает адрес редиректа для неавторизированных пользователей
    login_url = reverse_lazy('home')
    # будет генериться 403 (доступ запрещен) в случае неавторизированного юзера
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Добавление статьи')

        return context | c_def


# чтобы ограничить доступ для неавторизированных юзеров
@login_required
def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# вместо нее класс представления для отображения конкретной страницы (detailview)
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


# описание структуры наследования выше
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # изменяем названием переменной слага в маршрутизаторе
    slug_url_kwarg = 'post_slug'
    # в какую переменную будут помещаться данные из модели
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # будет нормально работать только в случае переопределения __str__ в классе
        # в остальных случаях лучше юзать context['post'].title
        c_def = self.get_user_context(title=context['post'])

        return context | c_def


# класс-представление вместо нее
# def show_category(request, cat_slug):
#     # сначала берем из базы айди категории по слагу
#     cat = Category.objects.filter(slug=cat_slug)
#     # достаем из полученного QuerySet по фильтру айдишник
#     cat_id = cat[0].pk
#     # потом находим посты по заданной категории
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'women/index.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # в случае, если в коллекции нет ни одной записи - ловим 404
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                    is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        # формируем контекст данный на осонве родительского (внутри коллекция записей)
        context = super().get_context_data(**kwargs)

        # обращаемся к параметру категории первой записи коллекции
        c_def = self.get_user_context(
            title='Категория - ' + str(context['posts'][0].cat),
            cat_selected=context['posts'][0].cat_id
        )

        return context | c_def


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# # имя параметра совпадает с его именем в маппинге
# def categories(request, catid):
#     if request.POST:
#         print(request.POST)
#
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>{catid}</p>')
#
#
# def archive(request, year):
#     if int(year) > 2020:
#         # автоматически перенаправляется на метод pageNotFound
#         # raise Http404()
#         # чтоб не хардкодить явный url адрес линки указывают его имя вместо пути
#         return redirect('home', permanent=True)
#
#     return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')
