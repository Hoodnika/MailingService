from datetime import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms

from clientapp.models import Client
from mainapp.models import MailingBody, MailingSettings, MailingReport


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingBodyForm(StyleFormMixin, forms.ModelForm):
    next = forms.CharField(required=False)

    class Meta:
        model = MailingBody
        fields = ('topic_mail', 'body_mail')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'next' in self.fields:
            self.fields['next'].widget = forms.HiddenInput()


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MailingSettingsForm, self).__init__(*args, **kwargs)
        self.fields['to_clients'].queryset = Client.objects.filter(owner=user)
        self.fields['message'].queryset = MailingBody.objects.filter(owner=user)

    class Meta:
        model = MailingSettings
        fields = ('first_sending', 'last_sending', 'periodicity', 'to_clients', 'message')

        widgets = {
            'first_sending': DatePickerInput(),
            'last_sending': DatePickerInput(),
            'to_clients': forms.SelectMultiple(attrs={'size': 20}),
        }



class MailingReportForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingReport
        fields = ('last_attempt_time', 'status', 'response')
