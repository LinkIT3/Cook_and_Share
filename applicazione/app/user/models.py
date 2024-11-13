from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from .custom.validators import validate_image as vi

# Validators
valid_char_nickname = RegexValidator(r'^[0-9a-z._-]*$', "Only alphanumeric characters and the characters . - _ are allowed")
profile_pic_validators = [vi.validate_profile_image]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        if not nickname:
            raise ValueError("The Nickname field must be set")
        
        if not password:
            raise ValueError("The Password field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        
        try:
            user.full_clean()
            user.save(using=self._db)
        except ValidationError as e:
            raise e
        
        return user
    
    def create_superuser(self, email, nickname, password, **extra_fields):
        return self.create_user(email, nickname, password, is_staff=True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    nickname = models.CharField( 
        null=False, 
        blank=False, 
        unique=True, 
        db_index=True,
        validators=[
            MinLengthValidator(2), 
            valid_char_nickname
        ],
        max_length=20, 
        verbose_name="Nickname",
        error_messages={"unique": "This nickname is already used"}
    )
    
    email = models.EmailField(
        null=False, 
        blank=False, 
        unique=True, 
        db_index=True,
        verbose_name="Email", 
        error_messages={"unique": "This email is already used"}
    )
    
    first_name = models.CharField(
        null= True, 
        blank=True, 
        validators=[MinLengthValidator(2)], 
        max_length=30,
        verbose_name="First Name"
    )
    
    last_name = models.CharField(
        null=True, 
        blank=True, 
        validators=[MinLengthValidator(2)], 
        max_length=30,
        verbose_name="Last Name"
    )
    
    profile_pic = models.ImageField(
        null=True, 
        blank=True, 
        upload_to="profile_pics/", 
        validators=profile_pic_validators, 
        verbose_name="Profile Picture", 
        help_text="Picture used for the profile"
    )
    
    food_critic = models.BooleanField(default=False, db_index=True)
    
    followed = models.ManyToManyField(
        "self", 
        blank=True, 
        editable=False, 
        symmetrical=False, 
        related_name="followers"
    )
    
    liked_recipes = models.ManyToManyField(
        "recipe.Recipe", 
        blank=True, 
        editable=False, 
        symmetrical=False, 
        related_name="liked"
    )
    
    saved_recipes = models.ManyToManyField(
        "recipe.Recipe", 
        blank=True, 
        editable=False, 
        symmetrical=False, 
        related_name="saved"
    )
    
    recipes_created = models.ManyToManyField(
        "recipe.Recipe", 
        blank=True,
        db_index=True,
        related_name="author", 
        verbose_name="Recipes created"
    )
    
    # For the recommendation system
    favorite_ingredients = models.JSONField(default=dict, blank=True)
    
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "password"]
    
    def update_profile_add(self, ingredients):
        for ingredient in ingredients:
            if ingredient in self.favorite_ingredients:
                self.favorite_ingredients[ingredient] += 1
            else:
                self.favorite_ingredients[ingredient] = 1
        
        self.save()
    
    
    def update_profile_remove(self, ingredients):
        for ingredient in ingredients:
            if ingredient in self.favorite_ingredients:
                if self.favorite_ingredients[ingredient] == 1:
                    self.favorite_ingredients.pop(ingredient)
                else:
                    self.favorite_ingredients[ingredient] -= 1
        
        self.save()
    
    
    def __str__(self) -> str:
        return str(self.nickname)
    
    
    class Meta():
        verbose_name_plural = "Users"