from django import forms

from blogapp.models import Blog, Comment
from mainapp.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['view_count', 'published', 'owner']

    def clean(self):
        """
        Проверяет все текстовые поля формы и проверяет на наличие запрещенных слов
        :return:
        """
        banned_words_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                             'радар', 'фурри']
        fields_list = []

        cleaned_data = super().clean()

        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField):
                fields_list.append(field_name)

        for field_data in fields_list:
            field_data = cleaned_data.get(field_data)
            for word in banned_words_list:
                if word in field_data.lower():
                    raise forms.ValidationError('Нельзя использовать запрещенные слова')

        return cleaned_data


class CommentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
