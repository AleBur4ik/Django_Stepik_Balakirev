from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5,
                            label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Короткий заголовок',
                                'required': 'Заголовок отсутствует'
                            })
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5, message='мало символов!!! минимум 5!'),
                               MaxLengthValidator(100, message='че так много!? максимум 100')
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False,
                              label='Контент')
    is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label='Категория не выбрана', label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False,
                                     empty_label='Не замужем', label='Муж')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только русские')
