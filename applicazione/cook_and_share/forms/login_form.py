from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        # self.helper.add_input(Submit('login', 'Login'))
        self.helper.layout = Layout(
            HTML("<div class='name-form mb-3 mt-4'>"),
                FloatingField('username', css_class='form-control', id="id_username"),
                FloatingField('password', css_class='form-control password-input', id="id_password"),
            HTML("</div>"),
            
            FormActions(
                Submit('login', 'Login', css_class='btn btn-primary', id="submit-btn"),
            ),
        )
        
    def clean(self):
        try:
            cleaned_data = super().clean()
        except forms.ValidationError:
            pass
        return self.cleaned_data