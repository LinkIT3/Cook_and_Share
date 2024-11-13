from django.test import TestCase
from django.urls import reverse

class TestReload(TestCase):
    def test_reload(self):
        response = self.client.get(reverse('reload'))
        
        self.assertRedirects(
            response,
            reverse('home')
        )