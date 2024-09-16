from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from .custom.validators import validate_image as vi

# Validators
valid_char_nickname = RegexValidator(r'^[0-9a-z._-]*$', "Only alphanumeric characters and the characters . - _ are allowed")
profile_pic_validators = [vi.validate_profile_image_size, vi.validate_image_extension, vi.validate_profile_image_dimension]


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
    
    nickname = models.CharField(verbose_name="Nickname", unique=True, null=False, blank=False, validators=[MinLengthValidator(2), valid_char_nickname], 
                                max_length=30, db_index=True, error_messages={"unique": "This nickname is already used"})
    
    email = models.EmailField(verbose_name="Email", unique=True, null=False, blank=False, db_index=True,
                                error_messages={"unique": "This email is already used"})
    
    first_name = models.CharField(verbose_name="First Name", null= True, blank=True, validators=[MinLengthValidator(2)], max_length=30)
    last_name = models.CharField(verbose_name="Last Name", null=True, blank=True, validators=[MinLengthValidator(2)], max_length=30)
    
    profile_pic = models.ImageField(verbose_name="Profile Picture", null=True, blank=True, upload_to="profile_pics/", validators=profile_pic_validators, 
                                    help_text="Picture used for the profile")
    
    food_critic = models.BooleanField(default=False, db_index=True)
    
    followed = models.ManyToManyField("self", editable=False, symmetrical=False, blank=True, related_name="followers")
    liked_recipes = models.ManyToManyField("recipe.Recipe", editable=False, symmetrical=False, blank=True, related_name="likes")
    recipes_created = models.ForeignKey("recipe.Recipe", on_delete=models.CASCADE, null=True, blank=True, 
                                        related_name="author", verbose_name="Recipes created", db_index=True)
    
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "password"]
    
    def __str__(self) -> str:
        return str(self.nickname)
    
    class Meta():
        verbose_name_plural = "Users"    
