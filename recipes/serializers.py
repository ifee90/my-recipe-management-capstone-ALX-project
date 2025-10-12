from rest_framework import serializers
from .models import Recipe, Ingredient

# Ingredient serializer
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'unit']

# Recipe serializer
class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)  # Nested ingredients
    author = serializers.ReadOnlyField(source='author.username')  # Show author's username

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'category',
            'preparation_time',
            'cooking_time',
            'servings',
            'created_at',
            'author',
            'ingredients',
        ]

    # Handle nested ingredients creation
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe
