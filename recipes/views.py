from rest_framework import generics, permissions
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer

# -----------------------------
# Recipe Views
# -----------------------------
class RecipeListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        category = self.request.query_params.get('category')
        ingredient = self.request.query_params.get('ingredient')

        # Filter by category (case-insensitive)
        if category:
            queryset = queryset.filter(category__iexact=category)

        # Filter by ingredient name (case-insensitive)
        if ingredient:
            queryset = queryset.filter(ingredients__name__icontains=ingredient)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionError("You can only update your own recipes.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionError("You can only delete your own recipes.")
        instance.delete()


# -----------------------------
# Ingredient Views
# -----------------------------
class IngredientListCreateView(generics.ListCreateAPIView):
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Ingredient.objects.all()

    def perform_create(self, serializer):
        serializer.save()  # Make sure to include recipe when posting


class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
