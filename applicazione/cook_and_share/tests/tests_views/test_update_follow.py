from django.test import TestCase
from django.urls import reverse

from app.user.models import CustomUser

import json


class TestUpdateFollow(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('toggle_follow'))
        
        self.assertEqual(
            response.status_code,
            405
        )
    
    
    def test_no_data(self):
        response = self.client.post(
            reverse('toggle_follow'), 
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_none_id(self):
        response = self.client.post(
            reverse('toggle_follow'),
            json.dumps({}),
            content_type='application/json'    
        )
        
        self.assertEqual(
            response.status_code,
            400
        )
    
    
    def test_no_user(self):
        response = self.client.post(
            reverse('toggle_follow'), 
            json.dumps({'user': 0}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_update_follow(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        user2 = CustomUser.objects.create_user(
            nickname='test_user2',
            email='testuser2@testuser2.com',
            password='test_user2'
        )
        user2.save()
        
        self.client.login(
            username='testuser@testuser.com', 
            password='test_user'
        )
        
        response = self.client.post(
            reverse('toggle_follow'), 
            json.dumps({'user': user2.id}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            201
        )
        
        response = self.client.post(
            reverse('toggle_follow'), 
            json.dumps({'user': user2.id}), 
            content_type='application/json'
        )
        
        self.assertEqual(
            response.status_code,
            201
        )