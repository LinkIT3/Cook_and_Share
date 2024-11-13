from django.forms import ValidationError
from django.test import TestCase

from cook_and_share.forms.settings_forms import PasswordForm
from app.user.models import CustomUser


class NameFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            nickname='test',
            email='test@test.com',
            password='test'
        )
        self.user.save()
    
    
    def test_form_valid(self):
        form = PasswordForm(
            data = {
                'old_password': 'test',
                'password': 'test1',
                'password_confirm': 'test1',
            },
            user = self.user
        )
        
        self.assertTrue(form.is_valid())
        form.save()
    
    
    def test_form_invalid_old_password(self):
        form = PasswordForm(
            data = {
            'old_password': 'test5',
            'password': 'test1',
            'password_confirm': 'test1',
            },
            user = self.user
        )
        
        self.assertFalse(form.is_valid())
    
    
    def test_form_invalid_password_confirm(self):
        form = PasswordForm(
            data = {
            'old_password': 'test',
            'password': 'test1',
            'password_confirm': 'test2',
            },
            user = self.user
        )
        
        self.assertFalse(form.is_valid())
    
    
    def test_null(self):
        with self.assertRaises(TypeError):
            form = PasswordForm()
            form.full_clean()