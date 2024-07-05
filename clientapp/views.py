from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from clientapp.forms import UserRegisterForm, UserLoginForm, UserProfileForm, ClientForm, UserResetPasswordForm, \
    UserPasswordResetConfirmForm
from clientapp.models import Client, User
from mainapp.services import send_mail_reg, send_auto_gen_password


class CustomLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = reverse_lazy('clientapp:login')
    redirect_field_name = 'redirect_to'


# CRUD для клиентов
class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.order_by('email')


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CustomLoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clientapp:client_list')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ClientCreateView, self).get_form_kwargs()
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
        return super(ClientCreateView, self).form_valid(form)

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('clientapp:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clientapp:client_list')


# Система авторизации, регистрации и восстановления пароля
class UserLoginView(LoginView):
    form_class = UserLoginForm


class UserPasswordResetView(PasswordResetView):
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('clientapp:password_reset_done')
    template_name = 'clientapp/password_reset_form.html'
    email_template_name = 'clientapp/password_reset_email.html'


def user_auto_generate_password(request):
    context = {
        'reset_message': 'Новый пароль отправлен на почту'
    }
    if request.method == 'POST':
        send_auto_gen_password(request, context)
    return render(request, 'clientapp/login.html', context)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name = 'clientapp/password_reset_confirm.html'
    success_url = reverse_lazy('clientapp:password_reset_complete')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'clientapp/register.html'
    success_url = reverse_lazy('clientapp:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        host = self.request.get_host()
        send_mail_reg(user, host)
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm

    success_url = reverse_lazy('clientapp:profile')

    def get_object(self):
        return self.request.user


class UserListView(ListView):
    model = User

    def get_queryset(self):
        return User.objects.order_by('email')
