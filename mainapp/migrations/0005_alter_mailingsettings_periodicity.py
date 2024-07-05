# Generated by Django 5.0.6 on 2024-07-04 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_mailingsettings_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='periodicity',
            field=models.CharField(choices=[('Раз в минуту(дебаг)', 'Five Sec'), ('Раз в день', 'Day'), ('Раз в неделю', 'Week'), ('Раз в месяц', 'Month'), ('По будням', 'Day Except Weekends')], max_length=21, verbose_name='периодичность отправки рассылки'),
        ),
    ]
