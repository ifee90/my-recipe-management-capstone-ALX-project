from django.db import models
from django.contrib.auth.models import User

# -----------------------------------------
# Recipe model
# -----------------------------------------
class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Dessert', 'Dessert'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    preparation_time = models.IntegerField(help_text="Time in minutes")
    cooking_time = models.IntegerField(help_text="Time in minutes")
    servings = models.IntegerField()
    cooking_method = models.TextField(
        blank=True,
        help_text="Describe the step-by-step cooking method or instructions."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # 👇 each recipe belongs to one user (the creator)
    owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='recipes',
    null=True,  # temporarily allow null for migration
    blank=True
)


# -----------------------------------------
# Ingredient model
# -----------------------------------------
class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)  # 👈 allows text like "2 cups" or "to taste"
    unit = models.CharField(max_length=50, blank=True)  # optional, can hold 'grams', 'cups', etc.


    def __str__(self):
        if self.recipe:
            return f"{self.quantity} {self.unit} {self.name} ({self.recipe.title})"
        return f"{self.name}"
