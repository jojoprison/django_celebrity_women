from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):

    # начальные свойста полей менются через конструктор
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        # делает связь с моедлью
        model = Women
        # какие поля отобразить в форме
        # __all__ - все поля, кроме заполняющихся автоматически
        # но рекомендуется явно указывать список полей
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # определяем стиль для виджетом формы
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # валидаторы должны начинаться с clean_
    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) > 200:
            raise ValidationError('Длина строки превышает 200 символов')

        return title


    # поля для формы без использования модели
    # title = forms.CharField(max_length=255, label='Заголовок',
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255, label='URL')
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
    #                           label='Контент')
    # is_published = forms.BooleanField(label='Публикация', required=False,
    #                                   initial=True)
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
    #                              empty_label='Категория не выбрана')
