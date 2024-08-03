from pyexpat import model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.apps import apps
from django.core.validators import MinLengthValidator, RegexValidator

from .custom.managers.CustomUserManager import CustomUserManager
from .custom.validators import validate_image as vi

valid_char_nickname = RegexValidator(r'^[0-9a-zA-Z._-]*$', "Only alphanumeric characters and the characters . - _ are allowed")
profile_pic_validators = [vi.validate_profile_image_size, vi.validate_image_extension, vi.validate_profile_image_dimension]




class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    nickname = models.CharField(unique=True, null=False, blank=False, validators=[MinLengthValidator(2), valid_char_nickname], 
                                max_length=30, db_index=True)
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    first_name = models.CharField(null= True, blank=True, validators=[MinLengthValidator(2)], max_length=30)
    last_name = models.CharField(null=True, blank=True, validators=[MinLengthValidator(2)], max_length=30)
    food_critic = models.BooleanField(default=False, db_index=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pics/", validators=profile_pic_validators, 
                                    verbose_name="Profile Picture", help_text="Picture used for the profile")
    followed = models.ManyToManyField("self", editable=False, symmetrical=False, related_name="followers")
    liked_recipes = models.ManyToManyField("recipe.Recipe", editable=False, symmetrical=False, related_name="likes")
    recipes_created = models.ForeignKey("recipe.Recipe", on_delete=models.CASCADE, related_name="author",
                                verbose_name="Recipes created", db_index=True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "password"]

    def __str__(self) -> str:
        return str(self.nickname)

    def Meta() -> None:
        verbose_name_plural = "Users"
    
""" Creazione Utente

user = User.objects.create_user(
    nickname="jhon",
    email='john@example.com',
    password='password123',
    first_name='John',
    last_name='Doe',
    )

print(user.nickname)  # jhon
print(user.email)  # john@example.com
print(user.first_name)  # John
print(user.last_name)  # Doe
"""