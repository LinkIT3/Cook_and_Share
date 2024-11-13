from django.test import TestCase
from django.urls import reverse

from app.user.models import CustomUser

import json

class TestLoadUserCard(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('load_user_card'))
        
        self.assertEqual(
            response.status_code,
            405
        )
    
    
    def test_invalid_json(self):
        response = self.client.post(reverse('load_user_card'))
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_user_id(self):
        response = self.client.post(
            reverse('load_user_card'),
            json.dumps({'test': 0}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_user(self):
        response = self.client.post(
            reverse('load_user_card'),
            json.dumps({'id': 0}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_user_card(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user',
            food_critic = True
        )
        user.save()
        
        self.client.login(
            username='testuser@testuser.com', 
            password='test_user'
        )
        
        response = self.client.post(
            reverse('load_user_card'),
            json.dumps({'id': user.id}),
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            200
        )