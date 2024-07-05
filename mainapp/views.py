from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from clientapp.models import Client
from clientapp.views import CustomLoginRequiredMixin
from mainapp.forms import MailingBodyForm, MailingSettingsForm
from mainapp.models import MailingBody, MailingSettings, MailingReport

from config.settings import TIME_ZONE, EMAIL_HOST_USER
from mainapp.services import check_first_date, send_with_create_or_update


# Главная страница
def index(request):
    if request.user.groups.filter(name='Manager').exists():
        body_list = MailingBody.objects.order_by('created_at')[:5]
        settings_list = MailingSettings.objects.order_by('first_sending')[:5]
        reports_list = MailingSettings.objects.filter(
            id__in=MailingReport.objects.values_list('mailing__id', flat=True)).order_by('first_sending')[:5]
        client_list = Client.objects.filter(owner=request.user.pk)
    else:
        body_list = MailingBody.objects.filter(owner=request.user.pk).order_by('created_at')[:5]
        settings_list = MailingSettings.objects.filter(owner=request.user.pk,
                                                       status__in=['Рассылка активна',
                                                                   'Рассылка остановлена']).order_by('first_sending')[
                        :5]
        reports_list = MailingSettings.objects.filter(owner=request.user.pk,
                                                      id__in=MailingReport.objects.values_list('mailing__id',
                                                                                               flat=True)).order_by(
            'first_sending')[:5]
        client_list = Client.objects.filter(owner=request.user.pk)

    context = {
        "body_list": body_list,
        "settings_list": settings_list,
        "report_list": reports_list,
        "client_list": client_list,

    }
    return render(request, 'mainapp/main.html', context)


# CRUD для MailingBody
class MailingBodyListView(ListView):
    model = MailingBody


class MailingBodyCreateView(CustomLoginRequiredMixin, CreateView):
    model = MailingBody
    form_class = MailingBodyForm
    success_url = reverse_lazy('mainapp:main')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(MailingBodyCreateView, self).get_form_kwargs()
        next_path = self.request.GET.get('next')
        if next_path:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': next_path})
            else:
                kwargs['initial'] = {'next': next_path}
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        redirect = form.cleaned_data.get('next')
        if redirect:
            self.success_url = redirect
        return super(MailingBodyCreateView, self).form_valid(form)


class MailingBodyDetailView(DetailView):
    model = MailingBody


class MailingBodyUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = MailingBody
    form_class = MailingBodyForm

    def get_success_url(self):
        return reverse_lazy('mainapp:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingBodyDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = MailingBody
    success_url = reverse_lazy('mainapp:main')


# CRUD для MailingSettings


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsCreateView(CustomLoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mainapp:main')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        clients = form.cleaned_data['to_clients']

        if check_first_date(form.instance.first_sending):
            form.instance.save()
            setting = form.instance
            send_with_create_or_update(setting, clients)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MailingSettingsCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class MailingSettingsUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    def get_success_url(self):
        return reverse_lazy('mainapp:main')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        clients = form.cleaned_data['to_clients']

        if check_first_date(form.instance.first_sending):
            form.instance.save()
            setting = form.instance
            send_with_create_or_update(setting, clients)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MailingSettingsUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingSettingsDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mainapp:main')


# CRUD для MailingReport


class MailingReportListView(ListView):
    model = MailingSettings


def report(request, pk):
    report_lst = MailingSettings.objects.filter(pk=pk).filter(
        id__in=MailingReport.objects.values_list('mailing__id', flat=True))
    context = {
        'report_list': report_lst,

    }
    return render(request, 'mainapp/report_detail.html', context)


def report_list(request):
    report_lst = MailingSettings.objects.filter(id__in=MailingReport.objects.values_list('mailing__id', flat=True))
    context = {
        'report_list': report_lst,

    }
    return render(request, 'mainapp/report_list.html', context)
