from django.db import models
from datetime import datetime

from clientapp.models import Client
from config.settings import AUTH_USER_MODEL
from mainapp.special_elements import NULLABLE


class MailingBody(models.Model):
    topic_mail = models.CharField(verbose_name='Тема письма', max_length=300)
    body_mail = models.TextField(verbose_name='Тело письма')
    created_at = models.DateTimeField(verbose_name='дата создания', default=datetime.now)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец письма', **NULLABLE)

    def __str__(self):
        return f'{self.topic_mail}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    class Periodicity(models.TextChoices):
        DAY = 'Раз в день'
        WEEK = 'Раз в неделю'
        MONTH = 'Раз в месяц'
        DAY_EXCEPT_WEEKENDS = 'По будням'

    class Status(models.TextChoices):
        STOPPED = 'Рассылка остановлена'
        IN_PROCESSING = 'Рассылка активна'
        COMPLETED = 'Рассылка завершена'

    first_sending = models.DateField(verbose_name='дата и время первой отправки рассылки', )
    last_sending = models.DateField(verbose_name='дата и время последней отправки рассылки', )
    periodicity = models.CharField(choices=Periodicity.choices, max_length=21,
                                   verbose_name='периодичность отправки рассылки')
    status = models.CharField(choices=Status.choices, max_length=20, verbose_name='статус рассылки',
                              default=Status.STOPPED)
    message = models.ForeignKey(MailingBody, on_delete=models.CASCADE, verbose_name='сообщение к отправке')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец рассылки', **NULLABLE)
    to_clients = models.ManyToManyField(Client, verbose_name='получатели рассылки', )

    def __str__(self):
        return f'Рассылка {self.message} - {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_deactivate_mailing', 'Может отключить рассылку')
        ]


class MailingReport(models.Model):
    class Status(models.TextChoices):
        SUCCESS = 'Успешно'
        FAIL = 'Не успешно'

    last_attempt_time = models.DateTimeField(verbose_name='дата и время последней попытки')
    status = models.CharField(choices=Status.choices, **NULLABLE, max_length=10,
                              verbose_name='статус попытки (успешно / не успешно')
    response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.mailing} - {self.last_attempt_time}'

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
