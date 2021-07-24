from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):

    # начальные свойста полей менются через конструктор
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        # делает связь с моделью
        model = Women
        # какие поля отобразить в форме
        # __all__ - все поля, кроме заполняющихся автоматически
        # но рекомендуется явно указывать список полей
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # определяем стиль для виджетов (поля, дариобаттоны, текстареи и тд.) формы
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


class RegisterUserForm(UserCreationForm):
    # продублируем переменные, чтобы у паролей корректно отображался стиль
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        # стандартный класс юзера
        model = User
        # поля, которые будут отображаться на форме
        fields = ('username', 'password1', 'password2')
        # оформление для каждого из полей
        widgets = {
            # добавляем еще класс оформления для полей формы
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


# форма для авторизации на сайт, класс Meta юзать не нужно, наследуемся с формы авторизации
class LoginUserForm(AuthenticationForm):
    # можно добавить дополнительные поля email, phone_number и тд
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    # можно создать кастомный класс капчи с родителем CaptchaTextInput
    captcha = CaptchaField()
