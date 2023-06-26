import os
from datetime import date
from io import BytesIO

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipe.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          TagSerializer)

font_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../static/fonts/arial.ttf')


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get']


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    http_method_names = ['get']


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        return self.delete_from_shopping_cart(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': 'Вы уже добавили рецепт в список покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from_shopping_cart(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт удален или не был добавлен в список покупок'},
            status=status.HTTP_400_BAD_REQUEST
        )

    from django.db.models import Sum

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipes = (
            ShoppingCart.objects
            .filter(user=user)
            .values(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit'
            )
            .annotate(amount=Sum('recipe__recipeingredient__amount'))
        )

        response = HttpResponse(content_type='application/pdf')
        username = user.username.replace(' ', '_')
        filename = f'{username}_shopping_cart.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdf.setFont('Arial', 12)

        # Оглавление
        pdf.drawString(100, 750, f"Список покупок для {username}")
        pdf.drawString(100, 730, f"Дата: {date.today().strftime('%Y-%m-%d')}")

        # Список ингредиентов
        y = 700
        for recipe in recipes:
            ingredient = recipe['recipe__ingredients__name']
            amount = recipe['amount']
            measurement_unit = recipe['recipe__ingredients__measurement_unit']
            ingredient_line = f"{ingredient} — {amount} ({measurement_unit})"
            pdf.drawString(100, y, ingredient_line)
            y -= 20

        y -= 20
        pdf.drawString(100, y, "from Foodgram")

        pdf.showPage()
        pdf.save()

        pdf_buffer = buffer.getvalue()
        buffer.close()
        response.write(pdf_buffer)

        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                serializer = RecipeShortSerializer(recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'Рецепт уже находится в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        try:
            favorite = Favorite.objects.get(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(
                {'message': 'Рецепт не находится в избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )
