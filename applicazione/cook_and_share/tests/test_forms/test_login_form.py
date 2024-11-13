from django.forms import ValidationError
from django.test import TestCase
from cook_and_share.forms.login_form import LoginForm
from app.user.models import CustomUser

class LoginFormTest(TestCase):
    def test_login_form(self):
        user = CustomUser.objects.create_user(
            nickname='test',
            email='test@test.com',
            password='test'
        )
        
        user.save()
        
        form = LoginForm(
            data = {
                'username': 'test@test.com', 
                'password': 'test'
            }
        )
        
        self.assertTrue(form.is_valid())
    
    
    def test_null_form(self):
        form = LoginForm()
        
        self.assertFalse(form.is_valid())
    
    
    def test_form_invalid(self):
        user = CustomUser.objects.create_user(
            nickname='test',
            email='test@test.com',
            password='test'
        )
        
        user.save()
        
        form = LoginForm(
            data = {
                'username': '', 
                'password': 'test1'
            }
        )
        
        self.assertFalse(form.is_valid())