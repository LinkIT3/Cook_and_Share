from django.test import TestCase
from django.urls import reverse

from app.ingredient.models import Ingredient
from app.recipe.models import Recipe

import json

class TestGetIngredients(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('get_ingredients'))
        self.assertEqual(
            response.status_code,
            405
        )
    
    def test_post_request_no_data(self):
        response = self.client.post(reverse('get_ingredients'))
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_post_request_with_data_no_id(self):
        response = self.client.post(
            reverse('get_ingredients'), 
            json.dumps({'test': 'test'}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_post_request_with_data_wrong_id(self):
        response = self.client.post(
            reverse('get_ingredients'), 
            json.dumps({'id': 100}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_post_request_with_data_all_ingredients(self):
        ingredient = Ingredient.objects.create(name='test')
        ingredient.save()
        
        
        response = self.client.post(
            reverse('get_ingredients'), 
            json.dumps({'id': 0}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertEqual(
            response.json(),
            ['test']
        )
    
    
    def test_post_request_with_data_id(self):
        ingredient = Ingredient.objects.create(name='test')
        ingredient.save()
        
        recipe = Recipe.objects.create(
            title='test',
            description='test',
            text='test',
            original_recipe=None,
            ingredient_quantity={str(ingredient): 1}
        )
        recipe.save()
        recipe.ingredient.add(ingredient)
        
        self.client.login(
            username='testuser@testuser.com', 
            password='test_user'
        )
        
        response = self.client.post(
            reverse('get_ingredients'), 
            json.dumps({'id': recipe.id}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
        
        self.assertEqual(
            response.json(),
            {'test': 1}
        )