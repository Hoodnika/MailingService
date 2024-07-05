from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path
from django.views.decorators.cache import cache_page

from clientapp.apps import ClientappConfig
from clientapp.views import UserLoginView, RegisterView, UserPasswordResetView, user_auto_generate_password, \
    ProfileView, UserPasswordResetConfirmView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    ClientDetailView, UserListView
from mainapp.services import email_confirm

app_name = ClientappConfig.name

urlpatterns = [
    path('client/', cache_page(20)(UserLoginView.as_view(template_name='clientapp/login.html')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', cache_page(20)(RegisterView.as_view()), name='register'),
    path('profile/', cache_page(20)(ProfileView.as_view()), name='profile'),
    path('email-confirm/<str:token_verification>/', email_confirm, name='email-confirm'),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/auto-generate/done/', user_auto_generate_password, name='password_reset_auto_generate_done'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='clientapp/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='clientapp/password_reset_complete.html'), name='password_reset_complete'),

    path('clients/', cache_page(20)(ClientListView.as_view()), name='client_list'),
    path('client/create/', cache_page(60)(ClientCreateView.as_view()), name='client_create'),
    path('client/<int:pk>/update/', cache_page(20)(ClientUpdateView.as_view()), name='client_update'),
    path('client/<int:pk>/delete/', cache_page(60)(ClientDeleteView.as_view()), name='client_delete'),
    path('client/<int:pk>/', cache_page(20)(ClientDetailView.as_view()), name='client_detail'),

    path('all-users/', cache_page(20)(UserListView.as_view()), name='user_list')
]
