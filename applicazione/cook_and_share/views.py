from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from datetime import timedelta

from thefuzz import fuzz

import random
import json

import logging

from app.ingredient.models import Ingredient
from app.recipe.models import Recipe
from app.recipe.forms.new_recipe import NewRecipeForm
from app.user.models import CustomUser

from .forms.login_form import LoginForm
from .forms.settings_forms import *


logger = logging.getLogger(__name__)

if settings.DEBUG:
    def set_admin(request):
        request.user.is_staff = True
        request.user.save()
        
        return redirect("home")


    def new_ingredient(request):
        nome = request.GET.get('nome')
        Ingredient.objects.create(name=nome)
        return redirect("home")


# Load the main pages
def load_page(request, recipe_id=None): 
    user = get_user(request)
    
    if not user.is_authenticated:
        return login_page(request)
    
    pic_path = "/media/default_profile_pic/default-profile-pic.webp"
    
    new_recipe_page = False
    remix = False
    edit = False
    
    user = get_user(request)
    
    if recipe_id != None:
        request.session['recipe_id'] = recipe_id
        request.session.save()
    
    if  request.session.get('recipe_id') != None and \
        request.session.get('recipe_id') > 0:
        
        if user.recipes_created.filter(id=request.session.get('recipe_id')).exists():
            edit = True
        
        else:
            remix = True
        
        recipe = Recipe.objects.get(pk=request.session.get('recipe_id'))
        
        new_recipe_page = True
    
    # New Recipe
    if remix:
        new_recipe_form = NewRecipeForm(
        request.POST or None, 
        request.FILES or None, 
        original_recipe=recipe
    )
    
    elif edit:
        new_recipe_form = NewRecipeForm(
            request.POST or None, 
            request.FILES or None, 
            instance=recipe
        )
    
    else:
        new_recipe_form = NewRecipeForm(
            request.POST or None, 
            request.FILES or None, 
            original_recipe=None
        )
    
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
        
        request.session['recipe_id'] = 0
        request.session.save()
        
        return redirect("recipe_page",  recipe_id=new_recipe.id)
    
    if  request.user.profile_pic != None and \
        request.user.profile_pic != "":
        
        pic_path = request.user.profile_pic.url
    
    context = {
        "nickname": request.user.nickname,
        "profile_pic_path": pic_path,
        "new_recipe_form": new_recipe_form,
        "new_recipe_page": new_recipe_page
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


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(   
            request, request.POST or None, 
            request.FILES or None
        )
        
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


# Return all the ingredients in the database
def get_ingredients(request):
    if request.method == 'POST':        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        
        if data.get('id') == None:
            return JsonResponse(
                {'error': 'Recipe ID not provided'}, 
                status=400
            )
        
        recipe_id = data.get('id')
        
        try:
            if recipe_id != 0:
                ingredients = Recipe.objects\
                    .get(pk=recipe_id)\
                    .ingredient_quantity
                return JsonResponse(ingredients)
            
            ingredients = Ingredient.objects.all()\
                .order_by('name')
        except Exception:
            return JsonResponse(
                {'error': 'Unable to get ingredients'}, 
                status=404
            )
        
        return JsonResponse(
            [ingredient.name for ingredient in ingredients], 
            safe=False
        )
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def log_out(request):
    logout(request)
    return redirect('home')


def reload(request):
    return redirect("home")


def load_user_card(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        
        if data.get('id') == None:
            return JsonResponse(
                {'error': 'User ID not provided'}, 
                status=400
            )
        
        user_id = data.get('id')
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except Exception:
            return JsonResponse(
                {'error': 'User not found'}, 
                status=404
            )
        
        food_critic = False
        follow = False
        same_user = True
        profile_pic_path = "/media/default_profile_pic/default-profile-pic.webp"
        
        if user.food_critic:
            food_critic = True
        
        if  user.profile_pic != None and \
            user.profile_pic != "":
            
            profile_pic_path = user.profile_pic.url
        
        if  request.user.is_authenticated and \
            request.user != user:
            
            same_user = False
        
        if  request.user.is_authenticated and \
            request.user.followed.filter(id=user.id).exists():
            
            follow = True
        
        
        html = render(
            request, 
            'user/card.html', { 
                'name': user.nickname,
                'user_id': user.id,
                'same_user': same_user,
                'food_critic': food_critic,
                'follow': follow,
                'profile_pic_path': profile_pic_path
            }
        ).content.decode('utf-8')
        
        return JsonResponse(
            {'html': html}, 
            status=200
        )
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def load_recipe_card(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        if data.get('id') == None:
            return JsonResponse(
                {'error': 'Recipe ID not provided'}, 
                status=400
            )
        
        recipe_id = data.get('id')
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Exception:
            return JsonResponse(
                {'error': 'Recipe not found'}, 
                status=404
            )
        
        author = recipe.author.all()[0]
        
        remix = True
        liked  = None
        saved = None
        
        if request.user.is_authenticated:
            
            liked = request.user.liked_recipes\
                .filter(id=recipe_id)\
                .exists()
            
            saved = request.user.saved_recipes\
                .filter(id=recipe_id).exists()
        
            if request.user.recipes_created\
                .filter(id=recipe_id).exists():
                
                remix = False
        
        
        link_recipe = "http://127.0.0.1:8000/recipe/" + \
            str(recipe_id) + "/" + \
            recipe.title.lower().replace(" ", "-")
        
        pdf_name = recipe.title.lower().replace(" ", "-") + \
            "_by_" + author.nickname + ".pdf"
        
        html = render(
            request, 
            'recipe/card/card.html', {   
                'recipe': recipe, 
                'author': author,
                'liked': liked,
                'saved': saved,
                'link_recipe': link_recipe,
                'remix': remix,
                'pdf_name': pdf_name
            }
        ).content.decode('utf-8')
        
        return JsonResponse(
            {'html': html}, 
            status=200
        )
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def getRecipes(request):
    if request.method == 'POST':
        
        results = []
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        if data.get('page') == None:
            return JsonResponse(
                {'error': 'Page number not provided'}, 
                status=400
            )
        
        page_number = data.get('page')
        
        if data.get('type') == None:
            return JsonResponse(
                {'error': 'Page type not provided'}, 
                status=400
            )
        
        page_type = data.get('type')
        
        match page_type:
            case 'home':
                user_ingredients = set(request.user.favorite_ingredients.keys())
                
                recommended_recipes = []
                
                for recipe in Recipe.objects\
                    .exclude(author=request.user) \
                    .exclude(
                        id__in=request.user.liked_recipes.all()\
                        .values_list('id', flat=True)
                    ) \
                    .exclude(
                        id__in=request.user.saved_recipes.all()\
                        .values_list('id', flat=True)
                    ) \
                    .distinct():
                    
                    common_ingredients = user_ingredients\
                        .intersection(
                            recipe.ingredient.all()\
                                .values_list('name', flat=True)
                        )
                    
                    similarity_score = 0
                    
                    if len(common_ingredients) > 0:
                        similarity_score = len(common_ingredients) / len(user_ingredients)
                    
                    if similarity_score > 0:
                        recommended_recipes.append((recipe, similarity_score))
                
                recommended_recipes.sort(key=lambda x: x[1], reverse=True)
                
                results = [recipe for recipe, _ in recommended_recipes[:500]]
                
                if len(results) < 500:
                    other_recipes = Recipe.objects \
                        .all() \
                        .exclude(author=request.user) \
                        .exclude(
                            id__in=request.user.liked_recipes.all()\
                            .values_list('id', flat=True)
                        ) \
                        .exclude(
                            id__in=request.user.saved_recipes.all()\
                            .values_list('id', flat=True)
                        ) \
                        .annotate(num_likes=Count('liked')) \
                        .order_by('-num_likes', '-last_edit_date')
                    
                    if len(results) + len(other_recipes) > 500:
                        other_recipes = other_recipes[:500 - len(results)]
                    
                    for recipe in other_recipes:
                        results.insert(
                            random.randint(0, len(results)),
                            recipe
                        )
                
                results = Recipe.objects.filter(id__in=set(recipe.id for recipe in results))
            
            
            case 'trending':
                results = Recipe.objects\
                    .filter(
                        last_edit_date__gte=(
                            timezone.now() - timedelta(days=7)
                        )
                    ) \
                    .annotate(
                        num_likes=Count('liked'), 
                        is_food_critic=Count(
                            'author__food_critic', 
                            filter=Q(author__food_critic=True)
                        )
                    ) \
                    .order_by(
                        '-num_likes', 
                        '-is_food_critic', 
                        '-last_edit_date'
                    )
            
            
            case 'last':
                results = Recipe.objects\
                    .filter(
                        last_edit_date__gte=(
                            timezone.now() - timedelta(days=1)
                        )
                    ) \
                    .order_by('-last_edit_date')
            
            
            case 'search-recipes':
                if data.get('search_string') == None:
                    return JsonResponse(
                        {'error': 'User Search String not provided'}, 
                        status=400
                    )
                
                search_string = data.get('search_string')
                
                if not search_string == "":
                    recipes = Recipe.objects.all()
                    
                    for recipe in recipes:
                        title_similarity = fuzz.ratio(
                            search_string.lower(), 
                            recipe.title.lower()
                        )
                        
                        ingredient_similarity = max(
                            [
                                fuzz.ratio(
                                    search_string.lower(), 
                                    ingredient.name.lower()
                                ) 
                                for ingredient in recipe.ingredient.all()
                            ],
                            default=0
                        )
                        
                        if  title_similarity >= 50 or \
                            ingredient_similarity >= 50:
                            
                            results.append(recipe)
                    
                    additional_results = Recipe.objects\
                        .filter(title__icontains=search_string) \
                        .exclude(id__in=[recipe.id for recipe in results])
                    
                    results.extend(additional_results)
                    
                    results_queryset = Recipe.objects\
                        .filter(id__in=set(recipe.id for recipe in results))
                    
                    results = results_queryset.annotate(
                        num_likes=Count('liked'),
                        num_saved=Count('saved'),
                        is_food_critic=Count(
                            'author__food_critic', 
                            filter=Q(author__food_critic=True)
                        )
                        
                    )\
                    .order_by(
                        '-num_likes', 
                        '-num_saved', 
                        '-is_food_critic'
                    )
            
            
            case 'search-users':
                if data.get('search_string') == None:
                    return JsonResponse(
                        {'error': 'User Search String not provided'}, \
                        status=400
                    )
                
                search_string = data.get('search_string')
                
                # results = CustomUser.objects.filter(
                #     Q(nickname__icontains=search_string) | 
                #     Q(first_name__icontains=search_string) |
                #     Q(last_name__icontains=search_string)
                # ).distinct().annotate(
                #     num_followers=Count('followers')
                # ).order_by('-num_followers', '-food_critic')
                
                
                if not search_string == "":
                    users = CustomUser.objects.all()
                    
                    for user in users:
                        nickname_similarity = fuzz.ratio(
                            search_string.lower(), 
                            user.nickname.lower()
                        )
                        
                        first_name_similarity = 0
                        last_name_similarity = 0
                        
                        if  user.first_name != None and \
                            user.first_name != '':
                            
                            first_name_similarity = fuzz.ratio(
                                search_string.lower(), 
                                user.first_name.lower()
                            )
                        
                        if  user.last_name != None and \
                            user.last_name != '':
                            
                            last_name_similarity = fuzz.ratio(
                                search_string.lower(), 
                                user.last_name.lower()
                            )
                        
                        if  nickname_similarity >= 40 or \
                            first_name_similarity >= 40 or \
                            last_name_similarity >= 40:
                            
                            results.append(user)
                    
                    results_queryset = CustomUser.objects\
                        .filter(id__in=set(user.id for user in results))
                    
                    results = results_queryset.annotate(
                        num_followers=Count('followers'),
                        is_food_critic=Count(
                            'food_critic', 
                            filter=Q(food_critic=True)
                        )
                    )\
                    .order_by(
                        '-num_followers', 
                        '-is_food_critic'
                    )
            
            
            case 'user':
                if data.get('user_id') == None:
                    return JsonResponse(
                        {'error': 'User ID not provided'}, 
                        status=400
                    )
                
                user_id = data.get('user_id')
                
                results = CustomUser.objects.get(id=user_id) \
                    .recipes_created.all() \
                    .order_by('-last_edit_date')
            
            
            case 'saved':
                if data.get('user_id') == None:
                    return JsonResponse(
                        {'error': 'User ID not provided'}, 
                        status=400
                    )
                
                user_id = data.get('user_id')
                
                results = CustomUser.objects.get(id=user_id) \
                    .saved_recipes.all() \
                    .order_by('-last_edit_date')
            
            
            case 'liked':
                if data.get('user_id') == None:
                    return JsonResponse(
                        {'error': 'User ID not provided'}, 
                        status=400
                    )
                
                user_id = data.get('user_id')
                
                results = CustomUser.objects.get(id=user_id) \
                    .liked_recipes.all() \
                    .order_by('-last_edit_date')
        
        results_per_page = 20
        results_list = []
        
        paginator = Paginator(results, results_per_page)
        page_obj = paginator.get_page(page_number)
        
        if len(results) > 0:
            results_list = list(page_obj.object_list.values())
        
        return JsonResponse({
            'results': results_list,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            
            'next_page_number': page_obj.next_page_number() 
                if page_obj.has_next() else None,
            
            'previous_page_number': page_obj.previous_page_number() 
                if page_obj.has_previous() else None
        }, status=200)
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def update_liked(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        
        if data.get('id') == None:
            return JsonResponse(
                {'error': 'Recipe ID not provided'}, 
                status=400
            )
        
        try:
            recipe = Recipe.objects.get(id=data.get('id'))
            
            if request.user.liked_recipes.filter(id=recipe.id).exists():
                request.user.liked_recipes.remove(recipe)
                request.user.update_profile_remove(
                    recipe.ingredient.all()\
                    .values_list('name', flat=True)
                )
            else:
                request.user.liked_recipes.add(recipe)
                request.user.update_profile_add(
                    recipe.ingredient.all()\
                    .values_list(
                        'name', 
                        flat=True
                    )
                )
            
            return JsonResponse(
                {'message': 'Like updated successfully'}, 
                status=201
            )
        
        except Recipe.DoesNotExist:
            return JsonResponse(
                {'error': 'Recipe not found'}, 
                status=404
            )
        
        except Exception as e:
            return JsonResponse(
                {'error': 'Unable to update like' + str(e)}, 
                status=404
            )
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def update_saved(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        if data.get('id') == None:
            return JsonResponse(
                {'error': 'Recipe ID not provided'}, 
                status=400
            )
        
        try:
            recipe = Recipe.objects.get(id=data.get('id'))
            
            if request.user.saved_recipes\
                .filter(id=recipe.id).exists():
                
                request.user.saved_recipes.remove(recipe)
                request.user.update_profile_remove(
                    recipe.ingredient.all()\
                    .values_list('name', flat=True)
                )
            else:
                request.user.saved_recipes.add(recipe)
                request.user.update_profile_add(
                    recipe.ingredient.all()\
                    .values_list('name', flat=True)
                )
            
            return JsonResponse(
                {'message': 'Save updated successfully'}, 
                status=201
            )
        
        except Recipe.DoesNotExist:
            return JsonResponse(
                {'error': 'Recipe not found'}, 
                status=404
            )
        
        except Exception:
            return JsonResponse(
                {'error': 'Unable to update save'}, 
                status=404
            )
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def update_follow(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        if data.get('user') == None:
            return JsonResponse(
                {'error': 'User ID not provided'}, 
                status=400
            )
        
        try:
            user = CustomUser.objects.get(id=data.get('user'))
            
            if request.user.followed.filter(id=user.id).exists():
                request.user.followed.remove(user)
            else:
                request.user.followed.add(user)
                
            return JsonResponse(
                {'message': 'Follow updated successfully'}, 
                status=201
            )
        
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'error': 'User not found'}, 
                status=404
            )
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def load_recipe_page(request, recipe_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON'}, 
                status=400
            )
        
        if data.get('id') == None:
            return JsonResponse(
                {'error': 'Recipe ID not provided'}, 
                status=400
            )
        
        recipe_id = data.get('id')
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return JsonResponse(
                {'error': 'Recipe not found'}, 
                status=404
            )
        
        try:
            author = recipe.author.all()[0]
        except Exception:
            return JsonResponse(
                {'error': 'Author not found'}, 
                status=404
            )
        
        html = render(request, 'recipe/page/page.html', {   
            'recipe': recipe,
            'author': author,
            'pdf': True
        }).content.decode('utf-8')
        
        return JsonResponse(
            {'html': html}, 
            status=200
        )
    
    recipe = Recipe.objects.get(id=recipe_id)
    author = recipe.author.all()[0]
    
    original_recipe = None
    original_recipe_link = None
    original_author = None
    
    if recipe.original_recipe != None:
        original_recipe = Recipe.objects.get(id=recipe.original_recipe.id)
        
        original_recipe_link = '/recipe/' + \
            str(original_recipe.id) + '/' + \
            original_recipe.title.lower().replace(" ", "-")
        
        original_author = original_recipe.author.all()[0]
    
    pic_path = "/media/default_profile_pic/default-profile-pic.webp"
    
    if  request.user.is_authenticated and \
        request.user.profile_pic != None and \
        request.user.profile_pic != "":
        
        pic_path = request.user.profile_pic.url
    
    context = { 
        'recipe': recipe,
        'author': author,
        'original_recipe': original_recipe,
        'original_recipe_link': original_recipe_link,
        'original_author': original_author,
        'profile_pic_path': pic_path
    }
    
    return render(request, 'recipe/page/page.html', context)


def user_page(request, nickname, index=False):
    user = CustomUser.objects.get(nickname=nickname)
    
    pic_path = "/media/default_profile_pic/default-profile-pic.webp"
    pic_path_navbar = "/media/default_profile_pic/default-profile-pic.webp"
    same_user = True
    follow = False
    
    profile_pic_form = None
    name_form = None
    password_form = None
    
    if  request.user.is_authenticated and \
        request.user.profile_pic != None and \
        request.user.profile_pic != "":
        
        pic_path_navbar = request.user.profile_pic.url
    
    if user.profile_pic != None and user.profile_pic != "":
        pic_path = user.profile_pic.url
    
    number_of_recipes_created = CustomUser.objects.filter(nickname=nickname) \
        .annotate(number_of_recipes=Count('recipes_created')).first()
    
    if request.user.id != user.id or \
        not request.user.is_authenticated:
        same_user = False
        
        if request.user.is_authenticated and \
            request.user.followed.filter(id=user.id).exists():
            follow = True
    
    if same_user:
        # Settings
        profile_pic_form = ProfilePicForm(
            request.POST or None, 
            request.FILES or None, 
            instance=request.user
        )
        
        name_form = NameForm(
            request.POST or None or None, 
            instance=request.user
        )
        
        password_form = PasswordForm(
            data=request.POST or None, 
            user=request.user
        )
        
        if "profile-pic-form" in request.POST and \
            profile_pic_form.is_valid():
            
            profile_pic_form.save()
            messages.success(
                request, 
                'Your profile picture is updated!'
            )
            return redirect("reload")
        
        if "name-form" in request.POST and \
            name_form.is_valid():
            
            name_form.save()
            messages.success(
                request, 
                'Your name is updated!'
            )
            return redirect("reload")
        
        if "password-form" in request.POST and \
            password_form.is_valid():
            
            password_form.save()
            messages.success(
                request, 
                'Your password is updateds!'
            )
            return redirect("profile")
    
    context = { 
        'user_page': user,
        'pic_path': pic_path,
        'profile_pic_path': pic_path_navbar,
        'same_user': same_user,
        'follow': follow,
        'number_of_recipes': number_of_recipes_created.number_of_recipes,
        "profile_pic_form": profile_pic_form,
        "name_form": name_form,
        "password_form": password_form
    }
    
    if index:
        return context
    
    return render(request, 'user/page.html', context)