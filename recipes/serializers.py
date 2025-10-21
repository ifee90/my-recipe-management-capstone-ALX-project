from rest_framework import serializers
from .models import Recipe, Ingredient


# -----------------------------------------
# Ingredient Serializer
# -----------------------------------------
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'unit']


# -----------------------------------------
# Recipe Serializer (includes cooking_method)
# -----------------------------------------
class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)
    owner = serializers.ReadOnlyField(source='owner.username')  # ✅ fixed from 'author' to 'owner'

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
            'cooking_method',
            'created_at',
            'owner',           # fixed from 'author'
            'ingredients',
        ]
        read_only_fields = ['owner', 'created_at']

    # Handle nested ingredient creation
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    # Handle nested ingredient updates
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ingredients_data is not None:
            instance.ingredients.all().delete()
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)
        return instance
