from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from app.ingredient.models import Ingredient
from app.recipe.models import Recipe
from app.user.models import CustomUser

import os
import json


class TestLoadRecipePage(TestCase):
    def get_image(self) -> SimpleUploadedFile:
        img_name = "test_image.png"
        
        img_path = os.path.join(os.path.dirname(__file__), img_name)
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file {img_path} not exist")
        
        with open(img_path, "rb") as img:    
            return SimpleUploadedFile(
                "test_image.png", 
                img.read(), 
                content_type="image/png"
            )
    
    
    def test_get_request(self):
        ingredient = Ingredient.objects.create(name='test')
        recipe = Recipe.objects.create(
            title='test',
            description='test',
            text='test',
            original_recipe=None,
            dish_pic=self.get_image(),
            ingredient_quantity={str(ingredient): 1}
        )
        recipe.save()
        recipe.ingredient.add(ingredient)
        
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        user.recipes_created.add(recipe)
        user.save()
        
        response = self.client.get(
            reverse(
                'recipe_page',
                kwargs={'recipe_id': recipe.id}
            ), 
        )
        
        self.assertTemplateUsed(
            response,
            'recipe/page/page.html'
        )
    
    
    
    def test_no_data(self):
        response = self.client.post(
            reverse(
                'recipe_page',
                kwargs={'recipe_id': 0}
            )
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_id(self):
        response = self.client.post(
            reverse(
                'recipe_page',
                kwargs={'recipe_id': 0}
            ), 
            json.dumps({}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_recipe(self):
        response = self.client.post(
            reverse(
                'recipe_page',
                kwargs={'recipe_id': 0}
            ), 
            json.dumps({'id': 0}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_recipe_no_author(self):
        recipe = Recipe.objects.create(
            title='test',
            description='test',
            text='test',
            original_recipe=None,
            dish_pic=self.get_image(),
            ingredient_quantity={}
        )
        recipe.save()
        
        response = self.client.post(
            reverse(
                'recipe_page',
                kwargs={'recipe_id': 0}
            ), 
            json.dumps({'id': recipe.id}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_recipe(self):
        ingredient = Ingredient.objects.create(name='test')
        recipe = Recipe.objects.create(
            title='test',
            description='test',
            text='test',
            original_recipe=None,
            dish_pic=self.get_image(),
            ingredient_quantity={str(ingredient): 1}
        )
        recipe.save()
        recipe.ingredient.add(ingredient)
        
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        user.recipes_created.add(recipe)
        user.save()
        
        response = self.client.post(
            reverse(
                'recipe_page',
                kwargs={'recipe_id': recipe.id}
            ), 
            json.dumps({'id': recipe.id}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertTemplateUsed(
            response,
            'recipe/page/page.html'
        )