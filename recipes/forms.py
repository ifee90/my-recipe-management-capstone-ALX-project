from django import forms
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'category',
            'preparation_time',
            'cooking_time',
            'servings',
            'cooking_method',   # ✅ corrected field
            'ingredients',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'cooking_method': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Step-by-step cooking instructions...'}),
            'category': forms.Select(choices=Recipe.CATEGORY_CHOICES),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit', 'recipe']
