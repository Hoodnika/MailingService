from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm

from clientapp.models import User, Client
from mainapp.forms import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):
    next = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'comment')
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Комментарий'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'next' in self.fields:
            self.fields['next'].widget = forms.HiddenInput()


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserResetPasswordForm(StyleFormMixin, PasswordResetForm):
    pass


class UserPasswordResetConfirmForm(StyleFormMixin, SetPasswordForm):
    pass
