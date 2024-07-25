from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from .custom.managers.CustomUserManager import CustomUserManager
from .custom.validators import validate_image as vi

valid_char_nickname = RegexValidator(r'^[0-9a-zA-Z._-]*$', "Only alphanumeric characters and the characters . - _ are allowed")
profile_pic_validators = [vi.validate_profile_image_size, vi.validate_image_extension, vi.validate_profile_image_dimensions]
dish_pic_validators = [vi.validate_dish_image_size, vi.validate_image_extension, vi.validate_dish_image_dimensions]


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(unique=True, null=False, blank=False, validators=[MinLengthValidator(2), valid_char_nickname], 
                                max_length=30, db_index=True)
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    first_name = models.CharField(null= True, blank=True, validators=[MinLengthValidator(2)], max_length=30)
    last_name = models.CharField(null=True, blank=True, validators=[MinLengthValidator(2)], max_length=30)
    food_critic = models.BooleanField(default=False, db_index=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pics/", validators=profile_pic_validators, 
                                    verbose_name="Profile Picture", help_text="Picture used for the profile")
    followed = models.ManyToManyField("self", null=True, editable=False, symmetrical=False, related_name="followers")
    liked_recipes = models.ManyToManyFieldy("Recipe", null=True, editable=False, symmetrical=False, related_name="likes")

    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "email", "password"]

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


class Recipe():
    name = models.CharField(null=False, blank=False, validators=[MinLengthValidator(2)], max_length=200, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes",
                                verbose_name="Author of the recipe", db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True ,verbose_name="Date and time when the recipe was published", editable=False)
    last_edit_date = models.DateTimeField(auto_now=True ,verbose_name="Date and time of the recipe last edited", editable=False)
    original_recipe = models.ForeignKey("self", null=True, blank=True, verbose_name="Original Recipe", 
                                        on_delete=models.SET_NULL, related_name="reimx", db_index=True)
    ingredient = models.ManyToManyField("Ingredient", related_name="recipes", symmetrical=True, editable=True, null=False, blank=False, db_index=True)
    text = models.TextField(null=False, blank=False, max_length=10000)
    dish_pic = models.ImageField(null=True, blank=True, upload_to="dish_pics/", validators=dish_pic_validators, 
                                    verbose_name="Dish Picture", help_text="Picture of the dish")
    
    def __str__(self) -> str:
        return str(self.name)
    
    def Meta() -> None:
        verbose_name_plural = "Recipes"
        
        

class Ingredient():
    name = models.CharField(null=False, blank=False, validators=[MinLengthValidator(2)], max_length=30, db_index=True)
    
    def __str__(self) -> str:
        pass
    
    def Meta() -> None:
        verbose_name_plural = "Ingredients"