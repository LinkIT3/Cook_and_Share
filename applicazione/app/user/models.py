from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from .custom.managers.CustomUserManager import CustomUserManager
from .custom.validators import validate_image as vi

valid_char = RegexValidator(r'^[0-9a-zA-Z._-]*$', "Only alphanumeric characters and the characters . - _ are allowed")

class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(validators=[MinLengthValidator(2), valid_char], max_length=30, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(validators=[MinLengthValidator(2)], max_length=30, blank=True)
    last_name = models.CharField(validators=[MinLengthValidator(2)], max_length=30, blank=True)
    food_critic = models.BooleanField(default=False)
    profile_pic = models.ImageField(blank=True, upload_to ='profile_pics/', validators=[vi.validate_image_dimensions, vi.validate_image_extension, vi.validate_image_size], verbose_name="Profile Picture", help_text="Picture used for the profile") #################
    followed = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    liked_recipes = models.ManyToManyFieldy("Ricetta", symmetrical=False, related_name="likes")

    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "email"]

    def __str__(self):
        return self.nickname


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