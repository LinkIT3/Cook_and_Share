from django.test import TestCase
from django.urls import reverse

from app.user.models import CustomUser

class TestLogOut(TestCase):
    def test_logout(self):
        
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
        
        response = self.client.get(reverse('logout'))
        
        self.assertRedirects(
            response,
            reverse('home')
        )