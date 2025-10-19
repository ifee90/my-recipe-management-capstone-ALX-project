from rest_framework import generics, permissions
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from .forms import RecipeForm, IngredientForm

# ----------------------------------------------------------
# API VIEWS (Django REST Framework)
# ----------------------------------------------------------

class RecipeListCreateView(generics.ListCreateAPIView):
    """List all recipes or create a new one."""
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        category = self.request.query_params.get('category')
        ingredient = self.request.query_params.get('ingredient')
        if category:
            queryset = queryset.filter(category__iexact=category)
        if ingredient:
            queryset = queryset.filter(ingredients__name__icontains=ingredient)
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific recipe."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            raise PermissionError("You can only update your own recipes.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionError("You can only delete your own recipes.")
        instance.delete()


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----------------------------------------------------------
# TEMPLATE-BASED VIEWS (Frontend)
# ----------------------------------------------------------

@login_required(login_url='login')
def recipe_list(request):
    """Homepage showing all recipes for logged-in users."""
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


@login_required(login_url='login')
def recipe_form(request, pk=None):
    """Handle creating and editing recipes."""
    recipe = get_object_or_404(Recipe, pk=pk) if pk else None

    # Ownership check for editing
    if recipe and recipe.owner != request.user:
        return redirect('recipe-list')

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            if not recipe:
                new_recipe.owner = request.user
            new_recipe.save()
            form.save_m2m()
            return redirect('recipe-list')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {'form': form})


@login_required(login_url='login')
def recipe_delete(request, pk):
    """Delete a recipe after confirmation."""
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.owner != request.user:
        return redirect('recipe-list')

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe-list')

    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})


@login_required(login_url='login')
def ingredient_form(request, recipe_id=None):
    """Add or edit ingredients linked to a recipe."""
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe-list')
    else:
        form = IngredientForm(initial={'recipe': recipe_id})
    return render(request, 'recipes/ingredient_form.html', {'form': form})


# ----------------------------------------------------------
# USER AUTHENTICATION (Signup, Login, Logout)
# ----------------------------------------------------------

def signup_view(request):
    """Handle new user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe-list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipe-list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    """Logout the user and redirect to login page."""
    logout(request)
    return redirect('login')
