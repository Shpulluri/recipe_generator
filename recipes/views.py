from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import requests
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SavedRecipe

# Home page


def home(request):
    return render(request, 'home.html')

# Index page: Add ingredients
@login_required
def index(request):
    return render(request, 'index.html')

# Recipe list page
def recipe_list(request):
    if request.method == "POST":
        ingredients = request.POST.get("ingredients", "")
        diet = request.POST.get("diet", "any")
        print("Ingredients:", ingredients)
        print("Diet preference:", diet)

        # Example: Replace with actual Spoonacular API call
        recipes = get_recipes_from_api(ingredients, diet)
        request.session['recipes'] = recipes
        return render(request, 'recipe_list.html', {'recipes': recipes})

        # Passing recipes to the template
    recipes = request.session.get('recipes',[])
    return render(request, "recipe_list.html", {"recipes": recipes})
    return render(request, "index.html")

# Recipe detail page
def recipe_detail(request, recipe_id):
    # Mock details for now (replace with dynamic data later)
    api_key = settings.SPOONACULAR_API_KEY
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    response = requests.get(url, params={"apiKey": api_key})
    if response.status_code == 200:
        recipe = response.json()
        return render(request, "recipe_detail.html", {"recipe": recipe})
    else:
        # Handle errors (e.g., invalid recipe ID, API error)
        return render(request, "recipe_detail.html", {"error": "Recipe details could not be fetched."})


'''def find_recipes(request):
    if request.method == "GET":
        return render(request,'index.html')

    if request.method == "POST":
        ingredients = request.POST.get("ingredients")  # Get ingredients from form input
        url = f"https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "ingredients": ingredients,
            "number": 10,  # Adjust the number of recipes returned
            "apiKey": API_KEY
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            recipes = response.json()
        else:
            recipes = []

        return render(request, 'recipe_list.html', {'recipes': recipes})'''


def get_recipes_from_api(ingredients, diet):
    api_key = settings.SPOONACULAR_API_KEY  # Get API key from settings
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients,
        'number': 10,
        'apiKey': api_key,
    }

    if diet.lower() != "any":
        params['diet'] = diet

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return [
            {
                'id': r['id'],
                'title': r['title'],
                'image': r.get('image', ''),
                'usedIngredients': [i['name'] for i in r['usedIngredients']],
                'missedIngredients': [i['name'] for i in r['missedIngredients']],
            }
            for r in response.json()
        ]
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return []

def nutrition(request, recipe_id):
    """
    Fetch nutritional information for a recipe by ID and display it on the nutrition page.
    """
    api_key = settings.SPOONACULAR_API_KEY
    # Fetch recipe information
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    response = requests.get(url, params={"apiKey": api_key})

    if response.status_code == 200:
        recipe = response.json()
        # Get the recipe summary
        summary = recipe.get("summary", "No summary available for this recipe.")
        return render(
            request,
            "nutrition.html",
            {
                "summary": summary,
                "recipe_id": recipe_id,
            },
        )
    else:
        # Handle case where recipe information couldn't be fetched
        error_message = "Recipe details could not be fetched."
        return render(request, "nutrition.html", {"summary": error_message})




def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login to continue')
            return redirect('login')  # Redirect to index page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        '''if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)'''
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user directly from the form
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')



        else:
            messages.error(request,'Invalid username or password.')


    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def save_recipe(request, recipe_id):
    if request.method == 'POST':
        # Fetch recipe details from Spoonacular API
        api_key = settings.SPOONACULAR_API_KEY
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        response = requests.get(url, params={"apiKey": api_key})

        if response.status_code == 200:
            recipe = response.json()

            # Check if recipe is already saved
            existing_saved_recipe = SavedRecipe.objects.filter(
                user=request.user,
                recipe_id=recipe_id
            ).first()

            if not existing_saved_recipe:
                SavedRecipe.objects.create(
                    user=request.user,
                    recipe_id=recipe_id,
                    recipe_title=recipe['title'],
                    recipe_image=recipe.get('image', '')
                )

            else:
                messages.error(request, 'Invalid username or password.')  # Handles form errors

            return redirect('index')

        return redirect('recipe_detail', recipe_id=recipe_id)


@login_required
def saved_recipes(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user)
    return render(request, 'index.html', {'saved_recipes': saved_recipes})
@login_required
def remove_saved_recipe(request, recipe_id):
    saved_recipe = get_object_or_404(SavedRecipe, user=request.user, recipe_id=recipe_id)
    saved_recipe.delete()
    return redirect('index')
