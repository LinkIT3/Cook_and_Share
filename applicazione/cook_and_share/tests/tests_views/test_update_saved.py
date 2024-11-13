from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from app.ingredient.models import Ingredient
from app.recipe.models import Recipe
from app.user.models import CustomUser

import os
import json


class TestUpdateSaved(TestCase):
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
        response = self.client.get(reverse('toggle_saved'))
        
        self.assertEqual(
            response.status_code,
            405
        )
    
    
    def test_no_data(self):
        response = self.client.post(reverse('toggle_saved'))
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_id_none(self):
        response = self.client.post(
            reverse('toggle_saved'), 
            json.dumps({}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_recipe(self):
        response = self.client.post(
            reverse('toggle_saved'), 
            json.dumps({'id': 0}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_update_saved(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        self.client.login(
            username='testuser@testuser.com', 
            password='test_user'
        )
        
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
        
        user.recipes_created.add(recipe)
        user.save()
        
        response = self.client.post(
            reverse('toggle_saved'), 
            json.dumps({'id': recipe.id}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            201
        )
        
        response = self.client.post(
            reverse('toggle_saved'), 
            json.dumps({'id': recipe.id}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            201
        )
