from django.db import models

from clientapp.models import User
from mainapp.special_elements import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Ссылка', unique=True)
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(**NULLABLE, upload_to='blogs/photo')
    published = models.BooleanField(verbose_name='Опубликовано', default=False)
    view_count = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец статьи', **NULLABLE)
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='дата последнего изменения', auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'


class Comment(models.Model):
    description = models.TextField(verbose_name='Комментарий')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='статья')
    created_at = models.DateField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='дата последнего изменения', auto_now=True)

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
