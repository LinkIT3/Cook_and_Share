from django import forms
from django.core.validators import MinLengthValidator
from django.forms import formset_factory
from django_select2 import forms as s2forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.recipe.models import Recipe
from app.user.models import CustomUser
from app.ingredient.models import Ingredient

class IngredientSelect2Widget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]

    def create_value(self, value):
        return self.get_queryset().get_or_create(name=value)[0]


class IngredientQuantityForm(forms.Form):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), empty_label=None)
    quantity = forms.CharField(required=True, label="Quantity")

IngredientQuantityFormSet = formset_factory(IngredientQuantityForm, extra=1)

class NewRecipeForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Dish Name", validators=[MinLengthValidator(2)], max_length=100)
    description = forms.CharField(required=True, label="Brief Description", validators=[MinLengthValidator(2)], max_length=300)
    text = forms.CharField(required=True, label="Recipe", validators=[MinLengthValidator(2)], max_length=50000, widget=forms.Textarea)
    ingredient_quantity = forms.CharField(widget=forms.HiddenInput())
    ingredient_formset = IngredientQuantityFormSet()
    ingredient = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=IngredientSelect2Widget
    )
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'text']
        
    
    def __init__(self, *args, **kwargs):
        super(NewRecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            
        )
        
        if kwargs.get('original_recipe'):
            original_recipe = kwargs.pop('original_recipe')
    
    def clean(self):
        ingredient_quantity = {}
        
        for form in self.cleaned_data['ingredient_formset']:
            ingredient_quantity[form.cleaned_data['ingredient']] = form.cleaned_data['quantity']
        
        self.cleaned_data['ingredient_quantity'] = ingredient_quantity