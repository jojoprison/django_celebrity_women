from django.db.models import Count

from women.models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
]


# обычно в джанге все дополнытельные вспомогательные классы объявляются
# в отедельном файле utils.py
# можно прописывать в миксине еще и общие аттрибуты
class DataMixin:
    # переменная для автоматической пагинации страниц - скок показывать
    paginate_by = 20

    # как раз будет создавать контекст для шаблона (он дублировался в других вьюхах)
    def get_user_context(self, **kwargs):

        # сформируем начальный словарь из именнованых параметров, которые передаются
        context = kwargs

        # избравляемся от тегов templatetags/show_categories и меняем шаблон base.html
        # считаем, сколько для каждой рубрики есть записей
        cats = Category.objects.annotate(Count('women'))
        # передаем список категорий, чтобы потом использовать на вьюхе через переменную
        context['cats'] = cats

        # делаем копию словаря с меню
        user_menu = menu.copy()
        # наш класс связан с конректным запросом - обращаемся через переменную
        # request к объекту user и смотрим, авторизирован ли он
        if not self.request.user.is_authenticated:
            # удаляем из меню второй пункт
            user_menu.pop(1)

        # формируем контекст для меню, чтоб корректно его отображать
        context['menu'] = user_menu

        # если мы уже как-то его передали - не переопределяем
        if 'cat_selected' not in context:
            # ставим значение 0 по умолчанию
            context['cat_selected'] = 0

        return context
