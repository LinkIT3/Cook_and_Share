from django.test import TestCase

from cook_and_share.forms.settings_forms import NameForm


class NameFormTest(TestCase):
    def test_name_form(self):
        form = NameForm({
            'first_name': 'test',
            'last_name': 'test',
        })
        
        self.assertTrue(form.is_valid())
        form.save()
        
        self.assertEqual(form.cleaned_data['first_name'], 'test')
        self.assertEqual(form.cleaned_data['last_name'], 'test')
    
    
    def test_null(self):
        form = NameForm()
        
        self.assertFalse(form.is_valid())