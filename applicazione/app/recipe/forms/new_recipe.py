from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML
from crispy_forms.bootstrap import FormActions

from app.recipe.models import Recipe
from app.ingredient.models import Ingredient


class NewRecipeForm(forms.ModelForm):
    dish_pic = forms.ImageField(label='Dish Picture', required=True)
    
    class Meta:
        model = Recipe
        fields = ['title','description', 'text', 'dish_pic', 'original_recipe']
        widgets = {'dish_pic': forms.FileInput(attrs={'id': 'id_dish_pic'})}
    
    def __init__(self, *args, **kwargs):
        original_recipe = kwargs.pop('original_recipe', None)

        super(NewRecipeForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].widget = forms.TextInput(attrs={'style': 'resize: none;'})
        self.fields['text'].label = 'Recipe'
        
        if original_recipe and original_recipe != None:
            self.fields['original_recipe'].initial = original_recipe.id
            self.fields['title'].initial = original_recipe.title
            self.fields['description'].initial = original_recipe.description
            self.fields['text'].initial = original_recipe.text
            self.fields['dish_pic'].initial = original_recipe.dish_pic
        else:
            self.fields['original_recipe'].initial = None
        
        
        self.helper = FormHelper()
        self.helper.form_method = "post"
        
        self.helper.layout = Layout(
            HTML("<div class='name-form mb-3 mt-4'>"),
                HTML("<div class='mb-3 title-div'>"),
                    Field('title', css_class='title-field'),
                HTML("</div>"),
                
                HTML("<div class='dish-pic-form mb-3'>"),
                    Field('dish_pic', css_class='form-control', id="formFile", accept=".avif, .jpg, .jpeg, .png, .webp"),
                HTML("</div>"),
                
                HTML("<div class='mb-3 description-div'>"),
                    Field('description', css_class='description-field'),
                HTML("</div>"),
                
                HTML("<div class='mb-3 text-div'>"),
                    Field('text', css_class='text-field'),
                HTML("</div>"),
                
                HTML("<div class='mb-3 ingredients-quantities-div' id='ingredient-list'>"),
                HTML("</div>"),
                
                HTML("<div class='mb-5 button-ingredient-container'>"),
                    HTML('<button type="button" id="add-ingredient" class="btn btn-outline-primary">Add Ingredient</button>'),                
                    HTML('<button type="button" id="remove-ingredient" class="btn btn-outline-danger">Remove Ingredient</button>'), 
                HTML("</div>"),
                
                FormActions(
                    Submit("new-recipe-form", 'Submit', css_class='btn btn-primary btn-lg', id="submit-btn"),
                ),
                
            HTML("</div>"),
        )
    
    
    def clean(self):
        cleaned_data = super().clean()
        ingredient_quantity = {}
        ingredients = []
        
        data = self.data
        non_declared_fields = {key: value for key, value in data.items() if key not in self.fields}
        
        for field_name in non_declared_fields.keys():
            if field_name.startswith('ingredients_'):
                quantity = non_declared_fields.get(f'quantities_{field_name.split("_")[1]}')
                value = non_declared_fields.get(field_name)
                
                if value and quantity:
                    try:
                        ingredient = Ingredient.objects.get(name=value)
                        
                    except Ingredient.DoesNotExist:
                        ingredient = Ingredient.objects.create(name=value)
                    
                    ingredients.append(ingredient)
                    ingredient_quantity[ingredient.name] = quantity
        
        cleaned_data['ingredients'] = ingredients
        cleaned_data['ingredient_quantity'] = ingredient_quantity    
        
        return cleaned_data