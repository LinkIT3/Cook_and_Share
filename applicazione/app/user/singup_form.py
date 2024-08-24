from django import forms
from app.user.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password1'}), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password2'}), label="Confirm Password")
    profile_pic = forms.ImageField(label='Profile Picture', required=False)
    
    
    class Meta:
        model = CustomUser
        fields = ["nickname", "email", "password", "password_confirm", "first_name", "last_name", "profile_pic"]
        widgets = {
            'nickname': forms.TextInput(attrs={'id': 'id_username'}),
            'email': forms.EmailInput(attrs={'id': 'id_email'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Sign Up"))
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
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
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_action = self.create_user()
    #     self.helper.add_input(Submit("submit", "Submit"))
        
    # nickname = forms.CharField()
    # email = forms.EmailField()
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # profile_pic = forms.ImageField()
    
    
    # def create_user(self):
    #     reverse_lazy("home")