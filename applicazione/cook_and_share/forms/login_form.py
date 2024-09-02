from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('login', 'Login'))
        
    def clean(self):
        try:
            cleaned_data = super().clean()
        except forms.ValidationError:
            pass  # Non fare nulla in caso di errore
        return self.cleaned_data