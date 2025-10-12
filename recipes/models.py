from django.db import models
from django.contrib.auth.models import User

# Recipe model
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
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Ingredient model
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"
