from django.test import TestCase
from django.urls import reverse

from app.user.models import CustomUser


class TestUserPage(TestCase):
    def test_user_page(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        response = self.client.get(
            reverse(
                "user_page", 
                kwargs={'nickname': user.nickname}
            )
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        
        self.assertTemplateUsed(
            response, 
            'user/page.html'
        )
        
        self.client.login(
            username='testuser@testuser.com', 
            password='test_user'
        )
        
        response = self.client.get(
            reverse(
                "user_page", 
                kwargs={'nickname': user.nickname}
            )
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        
        self.assertTemplateUsed(
            response, 
            'user/page.html'
        )