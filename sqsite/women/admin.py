from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# могут быть другие аттрибуты
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo',
              'is_published', 'time_create', 'time_update')
    # эти же поля для отображения должны присутствовать в списке fields
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    # чтоб кнопочки удалить сохранить и тд отображались сверху
    save_on_top = True

    def get_html_photo(self, object):
        # если фотки нет - джанга поставит прочерк
        if object.photo:
            # добавляем фильтр safe чтобы не экранировать теги
            return mark_safe(f"<img src='{ object.photo.url }' width=50")

    get_html_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # обязательно запятую, тк кортеж (если ее не поставить, будет тупо строка)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# первым параметром класс модели, вторым - вспомогаетльный класс
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

# меняем названия админ панели
admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах 2'
