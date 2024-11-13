from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from functools import partial
from app.user.custom.validators import validate_image as vi


dish_pic_validators = [vi.validate_dish_image]

def validate_max_length(value, max_length):
        if len(value) > max_length:
            raise ValidationError(f"This field cannot exceed {max_length} characters.")


class Recipe(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Date and time when the recipe was published"
    )
    
    last_edit_date = models.DateTimeField(
        auto_now=True, 
        editable=False,
        verbose_name="Date and time of the recipe last edited"
    )
    
    original_recipe = models.ForeignKey(
        "self", 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        db_index=True,
        related_name="reimx", 
        verbose_name="Original Recipe"
    )
    
    ingredient = models.ManyToManyField(
        "ingredient.Ingredient",
        blank=False,
        editable=True,  
        db_index=True,
        related_name="recipes"
    )
    
    ingredient_quantity = models.JSONField(default=dict) # {Ingredient: "str"}
    
    title = models.TextField(
        null=False, 
        blank=False, 
        validators=[
            MinLengthValidator(2),
            partial(validate_max_length, max_length=100)
        ], 
        max_length=100, 
        db_index=True
    )
    
    description = models.TextField(
        null=False, 
        blank=False, 
        validators=[
            MinLengthValidator(10),
            partial(validate_max_length, max_length=300)
        ], 
        max_length=300
    )
    
    text = models.TextField(
        null=False, 
        blank=False, 
        validators=[
            MinLengthValidator(100),
            partial(validate_max_length, max_length=50000)
        ], 
        max_length=50000
    )
    
    dish_pic = models.ImageField(
        null=True, 
        blank=True, 
        upload_to="dish_pics/", 
        validators=dish_pic_validators, 
        verbose_name="Dish Picture", 
        help_text="Picture of the dish")
    
    
    def __str__(self) -> str:
        return str(self.title)
    
    
    class Meta():
        verbose_name_plural = "Recipes"   
