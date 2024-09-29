from django import forms
from django.core.exceptions import ValidationError
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from app.user.models import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password1'}), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password2'}), label="Confirm Password")
    profile_pic = forms.ImageField(label='Profile Picture', required=False)
    
    
    class Meta:
        model = CustomUser
        fields = ["nickname", "email", "password", "password_confirm", "first_name", "last_name", "profile_pic"]
        widgets = {
            'nickname': forms.TextInput(attrs={'id': 'id_nickname'}),
            'email': forms.EmailInput(attrs={'id': 'id_email'}),
        }

    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            
            HTML("<div class='mb-3 mt-4'>"),
            FloatingField('nickname', css_class='form-control', id="id_nickname"),
            Div(id='nickname-feedback', css_class='invalid-feedback'),
            HTML("</div>"),
            
            HTML("<div class='mb-3'>"),
            FloatingField('email', css_class='form-control', id="id_email"),
            Div(id='email-feedback', css_class='invalid-feedback'),
            HTML("</div>"),
            
            HTML("<div class='mb-3'>"),
            FloatingField('password', css_class='form-control password-input', id="id_password1"),
            HTML("</div>"),
            
            HTML("<div class='mb-3'>"),
            FloatingField('password_confirm', css_class='form-control password-input', id="id_password2"),
            Div(id='password-feedback', css_class='invalid-feedback'),
            HTML("</div>"),
            
            HTML("<div class='mb-3'>"),
            Field('profile_pic', css_class='form-control', id="formFile", accept=".jpg, .jpeg, .png, .webp"),
            HTML("</div>"),
            
            HTML("<div class='mb-3'>"),
            FloatingField('first_name', css_class='form-control', id="id_first_name"),
            HTML("</div>"),
            
            HTML("<div class='mb-3'>"),
            FloatingField('last_name', css_class='form-control', id="id_last_name"),
            HTML("</div>"),
            
            FormActions(
                Submit('submit', 'Sign Up', css_class='btn btn-primary', id="submit-btn"),
            ),
        )
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        nickname = cleaned_data.get('nickname')
        email = cleaned_data.get('email')
        
        if nickname:
            nickname = nickname.lower()
        
        if CustomUser.objects.filter(nickname=nickname).exists():
            self.add_error('nickname', 'The nickname is already used')
        
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'The email is already used')
            
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'The password are different')
        
        return cleaned_data
    
    
    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            user.full_clean()
            
            if commit:
                user.save()
                
            return user
        except ValidationError as e:
            self.add_error(None, e)
            return None