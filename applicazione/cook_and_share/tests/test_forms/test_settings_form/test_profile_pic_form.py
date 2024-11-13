from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from cook_and_share.forms.settings_forms import ProfilePicForm

from PIL import Image, ImageChops

import os

class ProfilePicFormTest(TestCase):
    
    def get_image(self) -> SimpleUploadedFile:
        img_name = "test_image.png"
        
        img_path = os.path.join(os.path.dirname(__file__), "test_image", img_name)
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file {img_path} not exist")
        
        with open(img_path, "rb") as img:    
            return SimpleUploadedFile("test_image.png", img.read(), content_type="image/png")
    
    
    def test_valid_form(self):
        self.img = self.get_image()
        
        form = ProfilePicForm(files={'profile_pic': self.img})
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.assertFalse(
            ImageChops.difference(
                Image.open(self.img), 
                Image.open(form.cleaned_data['profile_pic'])
            ).getbbox(), 
            "The immages are different"
        )
    
    
    def test_null(self):
        form = ProfilePicForm()
        
        self.assertFalse(form.is_valid())
