from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from datetime import timedelta
from PIL import Image, ImageChops

import time

from app.recipe.models import Recipe
from app.ingredient.models import Ingredient

import os

class RecipeModelTests(TestCase):

    def get_image(self, high_weight=False, high_resolution=False, invalid_format=False, invalid_image=False) -> SimpleUploadedFile:
        img_name = "test_image.png"
        
        if high_weight:
            img_name = "test_image_high_weight.png"
        
        if high_resolution:
            img_name = "test_image_high_resolution.png"
        
        if invalid_format:
            img_name = "test_image_invalid_format.bmp"
        
        if invalid_image:
            img_name = "test.txt"
        
        img_path = os.path.join(os.path.dirname(__file__), "test_image", img_name)
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file {img_path} not exist")
        
        with open(img_path, "rb") as img:
            if invalid_image:
                return SimpleUploadedFile("test.txt", img.read(), content_type="text/plain")
            
            return SimpleUploadedFile("test_image.png", img.read(), content_type="image/png")
    
    
    def setUp(self):        
        self.ingredient = Ingredient(name="test")
        self.ingredient.save()
    
    
    def test_null(self):
        self.recipe_null = Recipe()
        
        with self.assertRaises(ValidationError):
            self.recipe_null.full_clean()
    
    
    def test_creation_date(self):
        self.recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe.save()
        self.recipe.ingredient.add(self.ingredient)
        
        self.assertLessEqual(timezone.now() - self.recipe.creation_date, timedelta(seconds=1), "Wrong creation datetime")
    
    
    def test_edit_date(self):
        self.recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe.save()
        self.date1 = self.recipe.last_edit_date
        self.recipe.ingredient.add(self.ingredient)
        time.sleep(0.5)
        self.recipe.title = "b" * 5
        self.recipe.save()
        
        self.assertNotEqual(self.recipe.last_edit_date, self.date1)
        self.assertLessEqual(timezone.now() - self.recipe.last_edit_date, timedelta(seconds=1), "Wrong edit datetime")
    
    
    def test_original_recipe_none(self):
        self.recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe.save()
        self.recipe.ingredient.add(self.ingredient)
        
        self.assertEqual(self.recipe.original_recipe, None)
    
    
    def test_original_recipe(self):
        self.recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe.save()
        self.recipe.ingredient.add(self.ingredient)
        
        self.recipe_remix = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
            original_recipe=self.recipe
        )
        self.recipe_remix.save()
        self.recipe.ingredient.add(self.ingredient)
        
        self.recipe.original_recipe = self.recipe_remix
        self.recipe.save()
        self.assertEqual(self.recipe.original_recipe, self.recipe_remix)
    
    
    def test_dish_pic(self):
        self.img = self.get_image()
        
        self.recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
            dish_pic=self.img
        )
        self.recipe.save()
        self.recipe.ingredient.add(self.ingredient)
        
        self.assertFalse(
            ImageChops.difference(
                Image.open(self.img), 
                Image.open(self.recipe.dish_pic)
            ).getbbox(), 
            "The immages are different"
        )
        
        with self.assertRaises(ValidationError):
            self.recipe = Recipe(
                ingredient_quantity={str(self.ingredient): 1},
                title="a" * 5,
                description="a" * 15,
                text="a" * 150,
                dish_pic=self.get_image(invalid_image=True)
            )
            self.recipe.save()
            self.recipe.ingredient.add(self.ingredient)
            self.recipe.full_clean()
        
        with self.assertRaises(ValidationError):
            self.recipe = Recipe(
                ingredient_quantity={str(self.ingredient): 1},
                title="a" * 5,
                description="a" * 15,
                text="a" * 150,
                dish_pic=self.get_image(high_weight=True)
            )
            self.recipe.save()
            self.recipe.ingredient.add(self.ingredient)
            self.recipe.full_clean()
        
        with self.assertRaises(ValidationError):
            self.recipe = Recipe(
                ingredient_quantity={str(self.ingredient): 1},
                title="a" * 5,
                description="a" * 15,
                text="a" * 150,
                dish_pic=self.get_image(high_resolution=True)
            )
            self.recipe.save()
            self.recipe.ingredient.add(self.ingredient)
            self.recipe.full_clean()
        
        with self.assertRaises(ValidationError):
            self.recipe = Recipe(
                ingredient_quantity={str(self.ingredient): 1},
                title="a" * 5,
                description="a" * 15,
                text="a" * 150,
                dish_pic=self.get_image(invalid_format=True)
            )
            self.recipe.save()
            self.recipe.ingredient.add(self.ingredient)
            self.recipe.full_clean()
    
    
    
    def test_title_minimum_length(self):
        self.recipe_title_min_len = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a",
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe_title_min_len.save()
        self.recipe_title_min_len.ingredient.add(self.ingredient)
        
        with self.assertRaises(ValidationError):
            self.recipe_title_min_len.full_clean()
    
    
    def test_title_maximum_length(self):
        self.recipe_title_max_len = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 110,
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe_title_max_len.save()
        self.recipe_title_max_len.ingredient.add(self.ingredient)
        
        with self.assertRaises(ValidationError):
            self.recipe_title_max_len.full_clean()
    
    
    def test_description_minimum_length(self):
        self.recipe_description_min_len = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a",
            text="a" * 150,
        )
        self.recipe_description_min_len.save()
        self.recipe_description_min_len.ingredient.add(self.ingredient)
        
        with self.assertRaises(ValidationError):
            self.recipe_description_min_len.full_clean()
    
    
    def test_description_maximum_length(self):
        self.recipe_description_max_len = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 310,
            text="a" * 150,
        )
        self.recipe_description_max_len.save()
        self.recipe_description_max_len.ingredient.add(self.ingredient)
        
        with self.assertRaises(ValidationError):
            self.recipe_description_max_len.full_clean()
    
    
    def test_text_minimum_length(self):
        self.recipe_text_min_len = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a",
        )
        self.recipe_text_min_len.save()
        self.recipe_text_min_len.ingredient.add(self.ingredient)
        
        with self.assertRaises(ValidationError):
            self.recipe_text_min_len.full_clean()
    
    
    def test_text_maximum_length(self):
        self.recipe_text_max_len = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 50010,
        )
        self.recipe_text_max_len.save()
        self.recipe_text_max_len.ingredient.add(self.ingredient)
        
        with self.assertRaises(ValidationError):
            self.recipe_text_max_len.full_clean()
    
    
    def test_str(self):
        self.recipe = Recipe(
            ingredient_quantity={str(self.ingredient): 1},
            title="a" * 5,
            description="a" * 15,
            text="a" * 150,
        )
        self.recipe.save()
        self.recipe.ingredient.add(self.ingredient)
        
        self.assertEqual(str(self.recipe), self.recipe.title)