from django import forms
from django.core.validators import MinLengthValidator
from django.forms import formset_factory
from django_select2 import forms as s2forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.recipe.models import Recipe
from app.ingredient.models import Ingredient
from django_select2.forms import ModelSelect2Widget



class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'text']

    def __init__(self, *args, **kwargs):
        super(NewRecipeForm, self).__init__(*args, **kwargs)

        # Aggiungiamo dinamicamente i campi per ingredienti e quantità
        self.fields['ingredients'] = forms.ModelChoiceField(
            queryset=Ingredient.objects.all(),
            label='Ingredient',
            required=True
        )
        self.fields['quantities'] = forms.CharField(
            label='Quantity',
            required=True
        )

    def clean(self):
        cleaned_data = super().clean()
        ingredient_quantity = {}

        ingredient_id = cleaned_data.get('ingredients')
        quantity = cleaned_data.get('quantities')

        if ingredient_id and quantity:
            try:
                # Controlla se l'ingrediente esiste nel database
                ingredient = Ingredient.objects.get(id=ingredient_id.id)
            except Ingredient.DoesNotExist:
                # Se non esiste, creiamo un nuovo ingrediente
                ingredient = Ingredient.objects.create(name=ingredient_id)

            # Memorizziamo l'ingrediente e la quantità come chiave-valore in un dizionario
            ingredient_quantity[ingredient.name] = quantity

        cleaned_data['ingredient_quantity'] = ingredient_quantity
        return cleaned_data
    
    
        # self.helper = FormHelper()
        # self.helper.form_method = "post"
        # self.helper.layout = Layout(
            
        # )
        
        # if kwargs.get('original_recipe'):
        #     original_recipe = kwargs.pop('original_recipe')
    
