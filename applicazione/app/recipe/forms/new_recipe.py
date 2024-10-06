from django import forms
from django.core.validators import MinLengthValidator
from django.forms import ModelChoiceField, formset_factory
from django_select2.forms import Select2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.recipe.models import Recipe
from app.ingredient.models import Ingredient

class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'text']
    
    def __init__(self, *args, **kwargs):
        super(NewRecipeForm, self).__init__(*args, **kwargs)
        
        if kwargs.get('original_recipe'):
            self.field['original_recipe'].initial = kwargs.pop('original_recipe')
        
        self.fields['title'].widget = forms.TextInput(attrs={'style': 'resize: none;'})
        self.fields['text'].label = 'Recipe'
        
        self.helper = FormHelper()
        self.helper.form_method = "post"
        
        self.helper.layout = Layout(
            HTML("<div class='name-form mb-3 mt-4'>"),
                HTML("<div class='mb-3 title-div'>"),
                    Field('title', css_class='title-field'),
                HTML("</div>"),
                
                HTML("<div class='mb-3 description-div'>"),
                    Field('description', css_class='description-field'),
                HTML("</div>"),
                
                HTML("<div class='mb-3 text-div'>"),
                    Field('text', css_class='text-field'),
                HTML("</div>"),
                
                HTML("<div class='mb-3 ingredients-quantities-div' id='ingredient-list'>"),
                HTML("</div>"),
                
                HTML("<div class='mb-3 button-ingredient-container'>"),
                    HTML('<button type="button" id="add-ingredient" class="btn btn-outline-primary">Add Ingredient</button>'),                
                    HTML('<button type="button" id="remove-ingredient" class="btn btn-outline-danger">Remove Ingredient</button>'), 
                HTML("</div>"),
                
                HTML("<div class='mb-3'></div>"),
                
                FormActions(
                    Submit("new-recipe-form", 'Submit', css_class='btn btn-primary', id="submit-btn"),
                ),
                
            HTML("</div>"),
            
            
        )
    
    def clean(self):
        cleaned_data = super().clean()
        ingredient_quantity = {}
        
        data = self.data
        print(data.items())
        non_declared_fields = {key: value for key, value in data.items() if key not in self.fields}
        print(non_declared_fields)
        for field_name in non_declared_fields.keys():
            
            if field_name.startswith('ingredients_'):
                quantity = non_declared_fields.get(f'quantities_{field_name.split("_")[1]}')

                value = non_declared_fields.get(field_name)
                if value and quantity:
                    print(value)
                    print(quantity)
                    try:
                        ingredient = Ingredient.objects.get(name=value)
                    except Ingredient.DoesNotExist:
                        ingredient = Ingredient.objects.create(name=value)
                        
                    ingredient_quantity[ingredient.name] = quantity
                    
        cleaned_data['ingredient_quantity'] = ingredient_quantity

            
        return cleaned_data

    
