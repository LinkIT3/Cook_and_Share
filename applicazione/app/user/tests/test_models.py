from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PIL import Image, ImageChops

import io
import os

from app.user.models import CustomUser
from app.recipe.models import Recipe


class CustomUserModelTests(TestCase):
    def get_image(self, high_weight=False, high_resolution=False, invalid_format=False, invalid_image=False) -> SimpleUploadedFile:
        img_name = "test_image.png"
        
        if high_weight:
            img_name = "test_image_high_weight.png"
        
        if high_resolution:
            img_name = "test_image_high_resolution.png"
        
        if invalid_format:
            img_name = "test_image_invalid_format.bmp"
        
        if invalid_image:
            img_name = "test.txt"
        
        img_path = os.path.join(os.path.dirname(__file__), "test_image", img_name)
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"The file {img_path} not exist")
        
        with open(img_path, "rb") as img:
            if invalid_image:
                return SimpleUploadedFile("test.txt", img.read(), content_type="text/plain")
            
            return SimpleUploadedFile("test_image.png", img.read(), content_type="image/png")
    

    def setUp(self):
        self.nickname = "test"
        self.email = "test@test.com"
        self.password = "test"
        self.first_name = "test"
        self.last_name = "test"
        
        self.user = CustomUser.objects.create_user(
            nickname=self.nickname,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
    
    
    def test_null(self):
        self.user_null = CustomUser()
        
        with self.assertRaises(ValidationError):
            self.user_null.full_clean()
    
    
    def test_nickname(self):
        self.assertEqual(self.user.nickname, self.nickname)
        
    
    
    def test_nickname_str(self):
        self.assertEqual(str(self.user), self.nickname)
    
    
    def test_email(self):
        self.assertEqual(self.user.email, self.email)
    
    
    def test_first_name(self):
        self.assertEqual(self.user.first_name, self.first_name)
    
    
    def test_last_name(self):
        self.assertEqual(self.user.last_name, self.last_name)
    
    
    def test_profile_pic(self):
        profile_pic = self.get_image()
        self.user.profile_pic = profile_pic
        self.user.save()
        
        self.assertFalse(
            ImageChops.difference(
                Image.open(profile_pic), 
                Image.open(self.user.profile_pic)
            ).getbbox(), 
            "The immages are different"
        )

        with self.assertRaises(ValidationError):
            self.user.profile_pic = self.get_image(invalid_image=True)
            self.user.save()
            self.user.full_clean()
        
        with self.assertRaises(ValidationError):
            self.user.profile_pic = self.get_image(high_weight=True)
            self.user.save()
            self.user.full_clean()
        
        with self.assertRaises(ValidationError):
            self.user.profile_pic = self.get_image(high_resolution=True)
            self.user.save()    
            self.user.full_clean()
        
        with self.assertRaises(ValidationError):
            self.user.profile_pic = self.get_image(invalid_format=True)
            self.user.save()
            self.user.full_clean()
    
    
    def test_no_nickname(self):
        with self.assertRaises(TypeError) or self.assertRaises(ValueError):
            self.user_no_nickname = CustomUser.objects.create_user(
                email=self.email,
                password=self.password
            )
    
    
    def test_none_nickname(self):
        with self.assertRaises(ValueError):
            self.user_no_nickname = CustomUser.objects.create_user(
                nickname=None,
                email=self.email,
                password=self.password
            )
    
    
    def test_no_email(self):
        with self.assertRaises(TypeError):
            self.user_no_email = CustomUser.objects.create_user(
                nickname=self.nickname,
                password=self.password
            )
    
    
    def test_wrong_email(self):
        with self.assertRaises(ValidationError):
            self.user_wrong_email = CustomUser.objects.create_user(
                nickname=self.nickname,
                email="test",
                password=self.password
            )
    
    
    def test_none_email(self):
        with self.assertRaises(ValueError):
            self.user_no_email = CustomUser.objects.create_user(
                nickname=self.nickname,
                email=None,
                password=self.password
            )
    
    
    def test_no_password(self):
        with self.assertRaises(TypeError):
            self.user_no_password = CustomUser.objects.create_user(
                nickname=self.nickname,
                email=self.email
            )
    
    
    def test_none_password(self):
        with self.assertRaises(ValueError):
            self.user_no_password = CustomUser.objects.create_user(
                nickname=self.nickname,
                email=self.email,
                password=None
            )
    
    
    def test_superuser(self):
        self.user_superuser = CustomUser.objects.create_superuser(
            nickname="superuser",
            email="superuser@superuser.com",
            password="superuser"
        )
        
        self.assertTrue(self.user_superuser.is_staff)
    
    
    def test_add_preference(self):
        self.user.update_profile_add(["test"])
        
        self.assertTrue("test" in self.user.favorite_ingredients)
        self.assertEqual(self.user.favorite_ingredients["test"], 1)
        
        self.user.update_profile_add(["test"])
        
        self.assertTrue("test" in self.user.favorite_ingredients)
        self.assertEqual(self.user.favorite_ingredients["test"], 2)
    
    
    def test_remove_preference(self):
        self.user.update_profile_add(["test"])
        self.user.update_profile_remove(["test"])
        
        self.assertFalse("test" in self.user.favorite_ingredients)
        
        self.user.update_profile_add(["test"])
        self.user.update_profile_add(["test"])
        
        self.user.update_profile_remove(["test"])
        self.assertEqual(self.user.favorite_ingredients["test"], 1)
    
    
    def test_food_critic(self):
        self.assertFalse(self.user.food_critic)
        
        self.user.food_critic = True
        self.user.save()
        
        self.assertTrue(self.user.food_critic)
    
    
    def test_followed(self):
        self.new_user = CustomUser.objects.create_user(
            nickname="new_user",
            email="newuser@newuser.com",
            password="new_user"
        )
        
        self.user.followed.add(self.new_user)
        
        self.assertTrue(self.new_user in self.user.followed.all())
        
        self.user.followed.remove(self.new_user)
        
        self.assertFalse(self.new_user in self.user.followed.all())
    
    
    def test_liked_recipes(self):
        self.recipe = Recipe(title="test")
        self.recipe.save()
        
        self.user.liked_recipes.add(self.recipe)
        
        self.assertTrue(self.recipe in self.user.liked_recipes.all())
        
        self.user.liked_recipes.remove(self.recipe)
        
        self.assertFalse(self.recipe in self.user.liked_recipes.all())
    
    
    def test_saved_recipes(self):
        self.recipe = Recipe(title="test")
        self.recipe.save()
        
        self.user.saved_recipes.add(self.recipe)
        
        self.assertTrue(self.recipe in self.user.saved_recipes.all())
        
        self.user.saved_recipes.remove(self.recipe)
        
        self.assertFalse(self.recipe in self.user.saved_recipes.all())
    
    
    def test_recipes_created(self):
        self.recipe = Recipe(title="test")
        self.recipe.save()
        
        self.user.recipes_created.add(self.recipe)
        
        self.assertTrue(self.recipe in self.user.recipes_created.all())
        
        self.user.recipes_created.remove(self.recipe)
        
        self.assertFalse(self.recipe in self.user.recipes_created.all())
    
    
    def test_str(self):
        self.assertEqual(str(self.user), self.nickname)