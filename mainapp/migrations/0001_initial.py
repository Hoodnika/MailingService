# Generated by Django 5.0.6 on 2024-07-01 15:41

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_mail', models.CharField(max_length=300, verbose_name='Тема письма')),
                ('body_mail', models.TextField(verbose_name='Тело письма')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата создания')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец письма')),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_sending', models.DateField(verbose_name='дата и время первой отправки рассылки')),
                ('last_sending', models.DateField(verbose_name='дата и время последней отправки рассылки')),
                ('periodicity', models.CharField(choices=[('1/12 * * * *', 'per 5 seconds'), ('0 13 * * *', 'per day'), ('0 13 * * 1', 'per week'), ('0 13 1 * *', 'per month'), ('0 13 * * 1-5', 'per day in work days')], max_length=20, verbose_name='периодичность отправки рассылки')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('In processing..', 'In Processing'), ('Completed', 'Completed')], default='Created', max_length=15, verbose_name='статус рассылки')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.mailingbody', verbose_name='сообщение к отправке')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец рассылки')),
                ('to_clients', models.ManyToManyField(to='clientapp.client', verbose_name='получатели рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_attempt_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата и время первой попытки')),
                ('last_attempt_time', models.DateTimeField(verbose_name='дата и время последней попытки')),
                ('status', models.CharField(blank=True, choices=[('Успешно', 'Success'), ('Не успешно', 'Fail')], max_length=10, null=True, verbose_name='статус попытки (успешно / не успешно')),
                ('response', models.TextField(blank=True, null=True, verbose_name='ответ почтового сервера')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.mailingsettings', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': 'Отчеты',
            },
        ),
    ]