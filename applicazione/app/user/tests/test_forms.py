from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.user.signup_form import SignUpForm

from PIL import Image, ImageChops

import os


class SignUpFormTest(TestCase):
    def get_image(self) -> SimpleUploadedFile:
        img_name = "test_image.png"
        
        img_path = os.path.join(os.path.dirname(__file__), "test_image", img_name)
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file {img_path} not exist")
        
        with open(img_path, "rb") as img:    
            return SimpleUploadedFile("test_image.png", img.read(), content_type="image/png")
    
    
    def setUp(self):
        self.data = {
            'nickname': "test",
            'email': "test@t.com",
            'password': "test",
            'password_confirm': "test",
            'first_name': "test",
            'last_name': "test"
        }
    
    
    def test_valid_form(self):
        self.img = self.get_image()
        
        form = SignUpForm(self.data, files={'profile_pic': self.img})
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.assertEqual(form.cleaned_data['nickname'], "test")
        self.assertEqual(form.cleaned_data['email'], "test@t.com")
        self.assertEqual(form.cleaned_data['first_name'], "test")
        self.assertEqual(form.cleaned_data['last_name'], "test")
        
        self.assertFalse(
            ImageChops.difference(
                Image.open(self.img), 
                Image.open(form.cleaned_data['profile_pic'])
            ).getbbox(), 
            "The immages are different"
        )
    
    
    def test_null_form(self):
        form = SignUpForm()
        
        self.assertFalse(form.is_valid())
    
    
    def test_same_nickname(self):        
        form = SignUpForm(self.data, files=None)
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.data['email'] = 'test1@t.com'
        
        form = SignUpForm(self.data, files=None)
        
        with self.assertRaises(ValueError or ValidationError):
            form.save()
    
    
    def test_same_email(self):        
        form = SignUpForm(self.data, files=None)
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.data['nickname'] = 'test1'
        form = SignUpForm(self.data, files=None)
        
        with self.assertRaises(ValueError or ValidationError):
            form.save()
    
    
    def test_password_not_match(self):
        self.data['password_confirm'] = 'test1'
        form = SignUpForm(self.data, files=None)
        
        with self.assertRaises(ValueError or ValidationError):
            form.save()