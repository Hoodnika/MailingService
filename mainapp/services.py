import secrets
import smtplib
from datetime import datetime, time

from django.core.mail import send_mail
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from crontab import CronTab

from clientapp.models import User
from config.settings import EMAIL_HOST_USER
from mainapp.models import MailingSettings, MailingReport


def ban_user(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = False
    user.save()
    prev_page = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(prev_page)


def check_first_date(first_sending):
    current_date = datetime.now().strftime("%d/%m/%Y")
    first_sending = first_sending.strftime("%d/%m/%Y")

    if current_date >= first_sending:
        return True


def check_last_date(last_sending):
    current_date = datetime.now().strftime("%d/%m/%Y")
    last_sending = last_sending.strftime("%d/%m/%Y")

    if current_date >= last_sending:
        return True


###########_EMAIL_SEND_############
def send_mail_reg(user, host):
    token_verification = secrets.token_hex(16)
    user.token_verification = token_verification
    url = f"http://{host}/email-confirm/{user.token_verification}"
    send_mail(
        subject="Подверждение регистрации",
        message=f"Подтвердите регистрацию, перейдя по ссылке\n{url}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=True,
    )


def email_confirm(request, token_verification):
    user = get_object_or_404(User, token_verification=token_verification)
    user.is_active = True
    user.token_verification = None
    user.save()
    return redirect(reverse('clientapp:login'))


def send_auto_gen_password(request, context):
    email = request.POST['email']
    user = User.objects.get(email=email)
    new_password = secrets.token_hex(8)
    user.set_password(new_password)
    user.save()
    send_mail(
        message=f'Вот ваш новый пароль - \n{new_password}',
        subject='Новый пароль',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_to_clients(mailing_settings):
    client_emails_list = []
    for setting in mailing_settings:
        for client in setting.to_clients.all():
            client_emails_list.append(client.email)

    for setting in mailing_settings:
        if check_first_date(setting.first_sending):
            try:
                send_mail(
                    subject=setting.message.topic_mail,
                    message=setting.message.body_mail,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=client_emails_list,
                    fail_silently=False,
                )
                MailingReport.objects.create(
                    last_attempt_time=datetime.now(),
                    status='Успешно',
                    response='Отправлено',
                    mailing=setting,
                )
            except smtplib.SMTPException as error:
                MailingReport.objects.create(
                    last_attempt_time=datetime.now(),
                    status='Не успешно',
                    response='Получатель не получил рассылку',
                    mailing=setting,
                )

        if check_last_date(setting.last_sending):
            setting.status = 'Рассылка завершена'
            setting.save()


def send_with_create_or_update(setting, clients):
    try:
        send_mail(
            subject=setting.message.topic_mail,
            message=setting.message.body_mail,
            from_email=EMAIL_HOST_USER,
            recipient_list=clients,
            fail_silently=False,
        )
        MailingReport.objects.create(
            last_attempt_time=datetime.now(),
            status='Успешно',
            response='Отправлено',
            mailing=setting,
        )
    except smtplib.SMTPException as error:
        MailingReport.objects.create(
            last_attempt_time=datetime.now(),
            status='Не успешно',
            response='Получатель не получил рассылку',
            mailing=setting,
        )


###########_CRONTAB_############

def send_mailing_per_day():
    mailing_settings = MailingSettings.objects.filter(status='Рассылка активна').filter(
        periodicity='Раз в день').prefetch_related('to_clients').all()

    send_to_clients(mailing_settings)


def send_mailing_per_week():
    mailing_settings = MailingSettings.objects.filter(status='Рассылка активна').filter(
        periodicity='Раз в неделю').prefetch_related('to_clients').all()
    send_to_clients(mailing_settings)


def send_mailing_per_month():
    mailing_settings = MailingSettings.objects.filter(status='Рассылка активна').filter(
        periodicity='Раз в месяц').prefetch_related('to_clients').all()
    send_to_clients(mailing_settings)


def send_mailing_per_day_except_weekend():
    mailing_settings = MailingSettings.objects.filter(status='Рассылка активна').filter(
        periodicity='По будням').prefetch_related('to_clients').all()
    send_to_clients(mailing_settings)


###########_ACTIVATE_OR_DEACTIVATE_############
def activate_mailing(request, pk):
    mailing_setting = MailingSettings.objects.get(pk=pk)
    mailing_setting.status = 'Рассылка активна'
    mailing_setting.save()
    prev_page = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(prev_page)


def deactivate_mailing(request, pk):
    mailing_setting = MailingSettings.objects.get(pk=pk)
    mailing_setting.status = 'Рассылка остановлена'
    mailing_setting.save()
    prev_page = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(prev_page)
