from django.db import models
from django.core.validators import MinLengthValidator

class Ingredient(models.Model):
    name = models.CharField(null=False, blank=False, validators=[MinLengthValidator(2)], max_length=30, db_index=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta():
        verbose_name_plural = "Ingredients"
