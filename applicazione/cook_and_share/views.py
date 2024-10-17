from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect

import json
import logging

from app.user.models import CustomUser
from app.recipe.models import Recipe
from app.ingredient.models import Ingredient

from .forms.login_form import LoginForm
from .forms.settings_forms import *
from app.recipe.forms.new_recipe import NewRecipeForm


logger = logging.getLogger(__name__)


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST, request.FILES)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.nickname}!")
                
                if user.is_staff:
                    return redirect('/admin/')
                
                return redirect('home')
            else:
                messages.error(request, "Incorrect username or password")
        else:
            messages.error(request, "Incorrect username or password")
    else:
        form = LoginForm()
    
    context = {
        "homepage": "last",
        "login_form": form,
    }
    
    return render(request, 'index.html', context)


def load_page(request):
    user = get_user(request)
    if user.is_authenticated:
        homepage = "home" 
        pic_path = "/media/default_profile_pic/default-profile-pic.webp"
        profile_pic_setted = False
        ingredients = Ingredient.objects.all().order_by('name')
        
        number_of_recipes_created = CustomUser.objects.filter(pk=request.user.id).annotate(number_of_recipes=Count('recipes_created')).first()
        
        if request.user.profile_pic != None and request.user.profile_pic != "":
            profile_pic_setted = True
            pic_path = request.user.profile_pic.url
        
        if request.method == 'POST':
            # Settings
            profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=request.user)
            name_form = NameForm(request.POST, instance=request.user)
            password_form = PasswordForm(data=request.POST, user=request.user)
            
            # New Recipe
            new_recipe_form = NewRecipeForm(request.POST, request.FILES, original_recipe=None)
            
            if "profile-pic-form" in request.POST and profile_pic_form.is_valid():
                profile_pic_form.save()
                messages.success(request, 'Your profile picture is updated!')
                return redirect("reload")
            
            if "name-form" in request.POST and name_form.is_valid():
                name_form.save()
                messages.success(request, 'Your name is updated!')
                return redirect("reload")
            
            if "password-form" in request.POST and password_form.is_valid():
                password_form.save()
                messages.success(request, 'Your password is updateds!')
                return redirect("profile")
            
            if "new-recipe-form" in request.POST and new_recipe_form.is_valid():
                recipe = new_recipe_form.save(commit=False)
                recipe.ingredient_quantity = new_recipe_form.cleaned_data['ingredient_quantity']
                ingredients_list = new_recipe_form.cleaned_data['ingredients']
                recipe.save()
                
                for ingredient in ingredients_list:
                    recipe.ingredient.add(Ingredient.objects.get(pk=ingredient.id))
                
                request.user.recipes_created.add(Recipe.objects.get(pk=recipe.id))
                messages.success(request, 'Your recipe is created!')

        else:
            profile_pic_form = ProfilePicForm()
            name_form = NameForm(instance=request.user)
            password_form = PasswordForm(user=request.user)    
            new_recipe_form = NewRecipeForm()
        
        context = {
            "homepage": homepage,
            "nickname": request.user.nickname,
            "profile_pic_setted": profile_pic_setted,
            "profile_pic_path": pic_path,
            "number_of_recipes": number_of_recipes_created.number_of_recipes,
            "profile_pic_form": profile_pic_form,
            "name_form": name_form,
            "password_form": password_form,
            "new_recipe_form": new_recipe_form,
            "ingredients": ingredients,
        }
        
        return render(request, 'index.html', context)
    
    return login_page(request)


def log_out(request):
    logout(request)
    return redirect('home')


def set_admin(request):
    request.user.is_staff = True
    request.user.save()
    
    return redirect("home")


def reload(request):
    return redirect("home")


def new_ingredient(request):
    nome = request.GET.get('nome')
    Ingredient.objects.create(name=nome)
    return redirect("home")

########################## 

def load_recipe_template(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    author = recipe.author.all()[0]
    liked = request.user.liked_recipes.filter(id=recipe_id).exists()
    saved = request.user.saved_recipes.filter(id=recipe_id).exists()
    link_recipe = "http://127.0.0.1:8000/recipe/" + str(recipe_id) + "/" + recipe.title.lower().replace(" ", "-")
    
    html = render(request, 'recipe/card/card.html', {   'recipe': recipe, 
                                                        'author': author,
                                                        'liked': liked,
                                                        'saved': saved,
                                                        'link_recipe': link_recipe
                                                    }).content.decode('utf-8')
    return JsonResponse({'html': html})



def getRecipes(request):
    # Query per ottenere tutti i risultati
    results = Recipe.objects.all()

    # Numero di risultati per pagina
    results_per_page = 4

    # Creare il paginatore
    paginator = Paginator(results, results_per_page)

    # Ottenere il numero della pagina corrente dall'URL
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Se la richiesta è AJAX, restituire i dati in formato JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results_list = list(page_obj.object_list.values())  # Trasforma i risultati in lista di dizionari
        return JsonResponse({
            'results': results_list,  # Lista dei risultati
            'has_next': page_obj.has_next(),  # Se c'è una pagina successiva
            'has_previous': page_obj.has_previous(),  # Se c'è una pagina precedente
            'current_page': page_obj.number,  # Numero della pagina corrente
            'total_pages': paginator.num_pages,  # Numero totale di pagine
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None
        })
    
    # Caricare il template se non è una richiesta AJAX
    return render(request, 'my_template.html', {'page_obj': page_obj})


def update_liked(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            recipe = Recipe.objects.get(id=data.get('id'))
            
            if request.user.liked_recipes.filter(id=recipe.id).exists():
                request.user.liked_recipes.remove(recipe)
            else:
                request.user.liked_recipes.add(recipe)
                
            return JsonResponse({'message': 'Like updated successfully'}, status=201)
        
        except Recipe.DoesNotExist:
            return JsonResponse({'error': 'Recipe not found'}, status=404)
        
        except Exception:
            return JsonResponse({'error': 'Unable to update like'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def update_saved(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            recipe = Recipe.objects.get(id=data.get('id'))
            
            if request.user.saved_recipes.filter(id=recipe.id).exists():
                request.user.saved_recipes.remove(recipe)
            else:
                request.user.saved_recipes.add(recipe)
                
            return JsonResponse({'message': 'Save updated successfully'}, status=201)
        
        except Recipe.DoesNotExist:
            return JsonResponse({'error': 'Recipe not found'}, status=404)
        
        except Exception:
            return JsonResponse({'error': 'Unable to update save'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)