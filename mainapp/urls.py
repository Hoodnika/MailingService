from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp.apps import MainappConfig
from mainapp.services import activate_mailing, deactivate_mailing, ban_user
from mainapp.views import index, MailingBodyCreateView, MailingBodyDetailView, MailingBodyUpdateView, \
    MailingBodyDeleteView, MailingBodyListView, MailingSettingsListView, MailingSettingsCreateView, \
    MailingSettingsDetailView, MailingSettingsUpdateView, MailingSettingsDeleteView, report, report_list

app_name = MainappConfig.name

urlpatterns = [
    path('main/', index, name='main'),
    path('activate_mailing/<int:pk>/', activate_mailing, name='activate_mailing'),
    path('deactivate_mailing/<int:pk>/', deactivate_mailing, name='deactivate_mailing'),
    path('ban_user/<int:pk>/', ban_user, name='ban'),

    path('message/all/', cache_page(20)(MailingBodyListView.as_view()), name='message_list'),
    path('message/create/', cache_page(60)(MailingBodyCreateView.as_view()), name='message_create'),
    path('message/<int:pk>/detail/', cache_page(60)(MailingBodyDetailView.as_view()), name='message_detail'),
    path('message/<int:pk>/update/', cache_page(60)(MailingBodyUpdateView.as_view()), name='message_update'),
    path('message/<int:pk>/delete/', cache_page(20)(MailingBodyDeleteView.as_view()), name='message_delete'),

    path('settings/all/', MailingSettingsListView.as_view(), name='setting_list'),
    path('settings/create/', cache_page(60)(MailingSettingsCreateView.as_view()), name='setting_create'),
    path('settings/<int:pk>/detail/', cache_page(60)(MailingSettingsDetailView.as_view()), name='setting_detail'),
    path('settings/<int:pk>/update/', cache_page(60)(MailingSettingsUpdateView.as_view()), name='setting_update'),
    path('settings/<int:pk>/delete/', cache_page(30)(MailingSettingsDeleteView.as_view()), name='setting_delete'),

    path('settings/all-report/', cache_page(60)(report_list), name='report_list'),
    path('settings/<int:pk>/report/', cache_page(60)(report), name='report'),

]
