from django.db import models
from django.core.validators import MinLengthValidator
from app.user.custom.validators import validate_image as vi


dish_pic_validators = [vi.validate_dish_image_size, vi.validate_image_extension, vi.validate_dish_image_dimension]

class Recipe(models.Model):
    name = models.CharField(null=False, blank=False, validators=[MinLengthValidator(2)], max_length=200, db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True ,verbose_name="Date and time when the recipe was published", editable=False)
    last_edit_date = models.DateTimeField(auto_now=True ,verbose_name="Date and time of the recipe last edited", editable=False)
    original_recipe = models.ForeignKey("self", null=True, blank=True, verbose_name="Original Recipe", 
                                        on_delete=models.SET_NULL, related_name="reimx", db_index=True)
    ingredient = models.ManyToManyField("ingredient.Ingredient", related_name="recipes", editable=True, blank=False, db_index=True)
    text = models.TextField(null=False, blank=False, max_length=10000)
    dish_pic = models.ImageField(null=True, blank=True, upload_to="dish_pics/", validators=dish_pic_validators, 
                                    verbose_name="Dish Picture", help_text="Picture of the dish")
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta():
        verbose_name_plural = "Recipes"
        
