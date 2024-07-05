from django.contrib import admin

from mainapp.models import MailingSettings, MailingBody, MailingReport


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('first_sending', 'periodicity', 'status', 'message')
    list_filter = ('first_sending', 'periodicity', 'status')


# @admin.register(MailingBody)
# class MailingBodyAdmin(admin.ModelAdmin):
#     list_display = ('topic_mail', 'body_mail')
#     list_filter = ('topic_mail',)
#     search_fields = ('topic_mail', 'body_mail')
#     ordering = ('topic_mail',)
#     list_per_page = 20
#     list_max_show_all = 100
#     list_editable = ('topic_mail', 'body_mail')
#     save_on_top = True
#     save_as_continue = True  #сохранение и продолжение редактирования


@admin.register(MailingReport)
class MailingReportAdmin(admin.ModelAdmin):
    list_display = ('last_attempt_time', 'status', 'response')
    list_filter = ('last_attempt_time', 'status')
    search_fields = ('last_attempt_time', 'status', 'response')
