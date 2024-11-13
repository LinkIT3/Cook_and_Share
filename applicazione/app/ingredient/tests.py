from django.core.exceptions import ValidationError
from django.test import TestCase
from app.ingredient.models import Ingredient

class IngredientModelTest(TestCase):
    
    def setUp(self):
        self.ingredient_none = Ingredient()
        self.ingredient_blank = Ingredient(name="")
        self.ingredient_min_lenght = Ingredient(name="a")
        self.ingredient_max_lenght = Ingredient(name="a" * 50)
        self.ingredient_lowercase = Ingredient(name="Garlic")
        self.ingredient = Ingredient(name="Basil")
    
    
    def test_null(self):
        with self.assertRaises(ValidationError):
            self.ingredient_none.full_clean()
    
    
    def test_blank(self):
        with self.assertRaises(ValidationError):
            self.ingredient_blank.full_clean()
    
    
    def test_minimum_length(self):
        with self.assertRaises(ValidationError):
            self.ingredient_min_lenght.full_clean()
    
    
    def test_maximum_lenght(self):
        with self.assertRaises(ValidationError):
            self.ingredient_max_lenght.full_clean()
    
    
    def test_name_is_lowercase(self):
        self.assertEqual(self.ingredient_lowercase.name, "garlic")
    
    
    def test_create_ingredient(self):
        self.assertEqual(self.ingredient.name, "basil")
        self.assertEqual(str(self.ingredient), "basil")