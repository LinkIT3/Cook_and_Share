from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.utils import timezone
from datetime import timedelta

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
        form = LoginForm(request, request.POST or None, request.FILES or None)
        
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


def load_page(request, recipe_id=None): 
    user = get_user(request)
    
    if not user.is_authenticated:
        return login_page(request)
    
    
    homepage = "home" 
    pic_path = "/media/default_profile_pic/default-profile-pic.webp"
    
    remix = False
    edit = False
    
    user = get_user(request)
    
    if recipe_id != None:
        request.session['recipe_id'] = recipe_id
        request.session.save()

    if request.session.get('recipe_id') != None and request.session.get('recipe_id') > 0:
        if user.recipes_created.filter(id=request.session.get('recipe_id')).exists():
            edit = True
        else:
            remix = True
    
        recipe = Recipe.objects.get(pk=request.session.get('recipe_id'))
    
    # New Recipe
    if remix:
        new_recipe_form = NewRecipeForm(request.POST or None, request.FILES or None, original_recipe=recipe)
    elif edit:
        new_recipe_form = NewRecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    else:
        new_recipe_form = NewRecipeForm(request.POST or None, request.FILES or None, original_recipe=None)
    
    if "new-recipe-form" in request.POST and new_recipe_form.is_valid():
        new_recipe = new_recipe_form.save(commit=False)
        new_recipe.ingredient_quantity = new_recipe_form.cleaned_data['ingredient_quantity']
        ingredients_list = new_recipe_form.cleaned_data['ingredients']
        new_recipe.save()
        
        for ingredient in ingredients_list:
            new_recipe.ingredient.add(Ingredient.objects.get(pk=ingredient.id))
        
        if remix:
            new_recipe.original_recipe = recipe
            messages.success(request, 'Your remix is created!')
        elif edit:
            messages.success(request, 'Your recipe is updated!')
        else:
            messages.success(request, 'Your recipe is created!')

        request.user.recipes_created.add(Recipe.objects.get(pk=new_recipe.id))

    if request.user.profile_pic != None and request.user.profile_pic != "":
        pic_path = request.user.profile_pic.url
    
    context = {
        "homepage": homepage,
        "page_to_show": homepage,
        "nickname": request.user.nickname,
        "profile_pic_path": pic_path,
        "new_recipe_form": new_recipe_form,
    }
    
    context.update(user_page(request, request.user.nickname, index=True))
    
    if edit or remix:
        context['page_to_show'] = 'new-recipe'
        context['id_recipe_to_edit_remix'] = recipe.id
        
        if edit:
            context["edit"] = True
        if remix:
            context["remix"] = True
    
    return render(request, 'index.html', context)

def get_ingredients(request, extra_path=None):
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            recipe_id = data.get('id')
        except KeyError:
            return JsonResponse({'error': 'Recipe ID not provided'}, status=400)
        
        try:
            if recipe_id != 0:
                ingredients = Recipe.objects.get(pk=recipe_id).ingredient_quantity
                return JsonResponse(ingredients)
            
            ingredients = Ingredient.objects.all().order_by('name')
        except Exception:
            return JsonResponse({'error': 'Unable to get ingredients'}, status=404)
        
        return JsonResponse([ingredient.name for ingredient in ingredients], safe=False)

    
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

def load_recipe_card(request, extra_path=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            recipe_id = data.get('id')
        except KeyError:
            return JsonResponse({'error': 'Recipe ID not provided'}, status=400)
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'error': 'Recipe not found'}, status=404)
        
        author = recipe.author.all()[0]
        liked = request.user.liked_recipes.filter(id=recipe_id).exists()
        saved = request.user.saved_recipes.filter(id=recipe_id).exists()
        link_recipe = "http://127.0.0.1:8000/recipe/" + str(recipe_id) + "/" + recipe.title.lower().replace(" ", "-")
        remix = True
        
        pdf_name = recipe.title.lower().replace(" ", "-") + "_by_" + author.nickname + ".pdf"
        
        if request.user.recipes_created.filter(id=recipe_id).exists():
            remix = False
            
        html = render(request, 'recipe/card/card.html', {   'recipe': recipe, 
                                                            'author': author,
                                                            'liked': liked,
                                                            'saved': saved,
                                                            'link_recipe': link_recipe,
                                                            'remix': remix,
                                                            'pdf_name': pdf_name
                                                        }).content.decode('utf-8')
        
        return JsonResponse({'html': html}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)




def getRecipes(request, extra_path=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            page_number = data.get('page')
        except KeyError:
            return JsonResponse({'error': 'Page number not provided'}, status=400)
        
        try:
            page_type = data.get('type')
        except KeyError:
            return JsonResponse({'error': 'Page type not provided'}, status=400)
        
        match page_type:
            case 'home':
                results = Recipe.objects.all().order_by('-last_edit_date')  #########################################################################################################################
            
            case 'trending':
                results = Recipe.objects.filter(last_edit_date__gte=(timezone.now() - timedelta(days=7))) \
                                        .annotate(num_likes=Count('liked')) \
                                        .order_by('-num_likes', '-last_edit_date')
            
            case 'last':
                results = Recipe.objects.filter(last_edit_date__gte=(timezone.now() - timedelta(days=1))) \
                                        .order_by('-last_edit_date')
            
            case 'search':
                pass
            
            case 'user':
                try:
                    user_id = data.get('user_id')
                except KeyError:
                    return JsonResponse({'error': 'User ID not provided'}, status=400)
                
                results = CustomUser.objects.get(id=user_id).recipes_created.all().order_by('-last_edit_date')

            case 'saved':
                try:
                    user_id = data.get('user_id')
                except KeyError:
                    return JsonResponse({'error': 'User ID not provided'}, status=400)
                
                results = CustomUser.objects.get(id=user_id).saved_recipes.all().order_by('-last_edit_date')
            
            case 'liked':
                try:
                    user_id = data.get('user_id')
                except KeyError:
                    return JsonResponse({'error': 'User ID not provided'}, status=400)
                
                results = CustomUser.objects.get(id=user_id).liked_recipes.all().order_by('-last_edit_date')
                
        results_per_page = 20

        paginator = Paginator(results, results_per_page)
        page_obj = paginator.get_page(page_number)

        results_list = list(page_obj.object_list.values())
        
        return JsonResponse({
            'results': results_list,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None
        }, status=200)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)


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


def load_recipe_page(request, recipe_id, extra_path=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            recipe_id = data.get('id')
        except KeyError:
            return JsonResponse({'error': 'Recipe ID not provided'}, status=400)
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse({'error': 'Recipe not found'}, status=404)
        
        try:
            author = recipe.author.all()[0]
        except Exception:
            return JsonResponse({'error': 'Author not found'}, status=404)

        html = render(request, 'recipe/page/page.html', {   'recipe': recipe,
                                                            'author': author,
                                                            'pdf': True
                                                        }).content.decode('utf-8')

        return JsonResponse({'html': html}, status=200)
    
    recipe = Recipe.objects.get(id=recipe_id)
    author = recipe.author.all()[0]
    original_recipe = None
    original_recipe_link = None
    original_author = None
    
    if recipe.original_recipe != None:
        original_recipe = Recipe.objects.get(id=recipe.original_recipe.id)
        original_recipe_link = '/recipe/' + str(original_recipe.id) + '/' + original_recipe.title.lower().replace(" ", "-")
        original_author = original_recipe.author.all()[0]
    
    context = { 'recipe': recipe,
                'author': author,
                'original_recipe': original_recipe,
                'original_recipe_link': original_recipe_link,
                'original_author': original_author
                }
    return render(request, 'recipe/page/page.html', context)



def user_page(request, nickname, index=False, extra_path=None):
    user = CustomUser.objects.get(nickname=nickname)
    
    pic_path = "/media/default_profile_pic/default-profile-pic.webp"
    same_user = True
    follow = False
    
    number_of_recipes_created = CustomUser.objects.filter(nickname=nickname).annotate(number_of_recipes=Count('recipes_created')).first()
        
    if user.profile_pic != None and user.profile_pic != "":
        pic_path = user.profile_pic.url
    
    if request.user.id != user.id:
        same_user = False
        
        if request.user.following.filter(id=user.id).exists():
            follow = True
    
    if same_user:
        # Settings
        profile_pic_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=request.user)
        name_form = NameForm(request.POST or None or None, instance=request.user)
        password_form = PasswordForm(data=request.POST or None, user=request.user)
        
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
        
        print(pic_path)
        
    context = { 'user': user,
                'profile_pic_path': pic_path,
                'same_user': same_user,
                'follow': follow,
                'number_of_recipes': number_of_recipes_created.number_of_recipes,
                "profile_pic_form": profile_pic_form,
                "name_form": name_form,
                "password_form": password_form,}
    
    if index:
        return context
        
    return render(request, 'user/page.html', context)