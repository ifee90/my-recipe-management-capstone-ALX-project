from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer

# List all recipes / Create a recipe
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Set the author to the logged-in user when creating
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Retrieve, Update, Delete a single recipe
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Only allow author to update or delete
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionError("You can only update your own recipes")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionError("You can only delete your own recipes")
        instance.delete()
