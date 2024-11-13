from django.test import TestCase
from django.urls import reverse

from app.user.models import CustomUser

import json

class TestGetRecipes(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('get_recipes'))
        
        self.assertEqual(
            response.status_code,
            405
        )
    
    
    def test_no_data(self):
        response = self.client.post(reverse('get_recipes'))
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_page(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps({'test': 0}),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_type(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps({'page': 0}),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_home(self):
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
        
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'home'
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_trending(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'trending'
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_last(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'last'
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_search_recipe_none(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'search-recipes',
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_serach_recipe(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'search-recipes',
                    'search_string': 'test'
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_search_users_none(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'search-users',
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_search_users(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'search-users',
                    'search_string': 'test_user'
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_user_none(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'user',
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_user(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'user',
                    'user_id': user.id
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_saved_none(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'saved',
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_saved(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'saved',
                    'user_id': user.id
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            200
        )
    
    
    def test_liked_none(self):
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0, 
                    'type': 'liked',
                }
            ),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_liked(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        response = self.client.post(
            reverse('get_recipes'),
            json.dumps(
                {
                    'page': 0,
                    'type': 'liked',
                    'user_id': user.id
                }
            ),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            200
        )