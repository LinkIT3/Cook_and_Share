from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from app.ingredient.models import Ingredient
from app.recipe.models import Recipe
from app.recipe.forms.new_recipe import NewRecipeForm

from PIL import Image, ImageChops

import os

class NewRecipeFormTest(TestCase):
    def get_image(self) -> SimpleUploadedFile:
        img_name = "test_image.png"
        
        img_path = os.path.join(os.path.dirname(__file__), "test_image", img_name)
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file {img_path} not exist")
        
        with open(img_path, "rb") as img:    
            return SimpleUploadedFile("test_image.png", img.read(), content_type="image/png")
    
    
    def setUp(self):
        pass
    
    
    def test_valid_form_new_recipe(self):
        self.img = self.get_image()
        
        data ={
            'title': 'a' * 5,
            'description': 'a' * 15,
            'text': 'a' * 100,
            'original_recipe': None,
            'ingredients_Tomato': 'Tomato',
            'quantities_Tomato': '2',
            'ingredients_Garlic': 'Garlic',
            'quantities_Garlic': '1',
        }
        
        form = NewRecipeForm(data, files={'dish_pic': self.img})
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.assertEqual(form.cleaned_data['title'], 'a' * 5)
        self.assertEqual(form.cleaned_data['description'], 'a' * 15)
        self.assertEqual(form.cleaned_data['text'], 'a' * 100)
        self.assertEqual(form.cleaned_data['original_recipe'], None)
        
        self.assertFalse(
            ImageChops.difference(
                Image.open(self.img), 
                Image.open(form.cleaned_data['dish_pic'])
            ).getbbox(), 
            "The immages are different"
        )
    
    
    def test_valid_form_remix_recipe(self):
        self.img = self.get_image()
        
        self.ingredient = Ingredient(name="Tomato")
        self.ingredient.save()
        
        self.original_recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 100,
            dish_pic=self.img
        )
        self.original_recipe.save()
        self.original_recipe.ingredient.add(self.ingredient)
        
        
        data ={
            'title': 'a' * 5,
            'description': 'a' * 15,
            'text': 'a' * 100,
            'ingredients_Tomato': 'Tomato',
            'quantities_Tomato': '1',
        }
        
        form = NewRecipeForm(data, files=None, original_recipe=self.original_recipe)
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.assertEqual(form.cleaned_data['title'], 'a' * 5)
        self.assertEqual(form.cleaned_data['description'], 'a' * 15)
        self.assertEqual(form.cleaned_data['text'], 'a' * 100)
        self.assertEqual(form.cleaned_data['original_recipe'], None)
        
        self.assertFalse(
            ImageChops.difference(
                Image.open(self.img), 
                Image.open(form.cleaned_data['dish_pic'])
            ).getbbox(), 
            "The immages are different"
        )
    
    
    def test_invalid_form(self):
        form = NewRecipeForm()
        
        self.assertFalse(form.is_valid())