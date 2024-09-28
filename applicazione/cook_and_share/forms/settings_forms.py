from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.user.models import CustomUser

class ProfilePicForm(forms.ModelForm):
    profile_pic = forms.ImageField(label='Profile Picture', required=False)
    
    class Meta:
        model = CustomUser
        fields = ['profile_pic']
        widgets = {'profile_pic': forms.FileInput(attrs={'id': 'id_profile_pic'})}
    
    def __init__(self, *args, **kwargs):
        super(ProfilePicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div class='profile-pic-form mb-3 mt-4'>"),
                Field('profile_pic', css_class='form-control', id="formFile", accept=".jpg, .jpeg, .png, .webp"),
            HTML("</div>"),
            
            FormActions(
                Submit('profile-pic-form', 'Submit', css_class='btn btn-primary', id="submit-btn"),
            ),
        )


class NameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'id': 'id_first_name'}),
        #     'last_name': forms.TextInput(attrs={'id': 'id_last_name'}),
        # }
    
    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div class='name-form mb-3 mt-4'>"),
                HTML("<div class='mb-3'>"),
                    FloatingField('first_name', css_class='form-control', id="id_first_name", initial=self.instance.first_name),
                HTML("</div>"),
                
                HTML("<div class='mb-3'>"),
                    FloatingField('last_name', css_class='form-control', id="id_last_name", initial=self.instance.last_name),
                HTML("</div>"),
            HTML("</div>"),
            
            FormActions(
                Submit("name-form", 'Submit', css_class='btn btn-primary', id="submit-btn"),
            ),
        )


class PasswordForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_old_password'}), label="Current Password")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password_new_1'}), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password_new_2'}), label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ["password", "password_confirm"]
        widgets = {
            'old_password': forms.PasswordInput(attrs={'id': 'id_old_password'}),
            'password': forms.PasswordInput(attrs={'id': 'id_password'}),
            'password_confirm': forms.PasswordInput(attrs={'id': 'id_password_confirm'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.user = user
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div class='name-form mb-3 mt-4'>"),
                HTML("<div class='mb-3'>"),
                    FloatingField('old_password', css_class='form-control', id="id_old_password"),
                HTML("</div>"),
                
                HTML("<div class='mb-3'>"),
                    FloatingField('password', css_class='form-control', id="id_password_new_1"),
                HTML("</div>"),
                
                HTML("<div class='mb-3'>"),
                    FloatingField('password_confirm', css_class='form-control', id="id_password_new_2"),
                    Div(id='password-feedback', css_class='invalid-feedback'),
                HTML("</div>"),    
            HTML("</div>"),
            
            FormActions(
                Submit('password-form', 'Sign Up', css_class='btn btn-primary', id="submit-btn-paswd"),
            ),
        )
    
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        
        if not self.user.check_password(old_password):
            raise ValidationError("La vecchia password non è corretta.")
        
        return old_password
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'The password are different')
        
        return cleaned_data
    
    
    def save(self, commit=True):
            self.user.set_password(self.cleaned_data["password"])
            
            if commit:
                self.user.save()
            
            return self.user