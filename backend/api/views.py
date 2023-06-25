from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser, Subscriber
from recipe.models import Tag, Ingredient, Recipe, ShoppingCart, RecipeIngredient
from .serializers import UserCreateSerializer, TagSerializer, IngredientSerializer, \
    RecipeSerializer, RecipeCreateSerializer, RecipeIngredientSerializer, SubscriberSerializer, \
    CustomUserSerializer, RecipeShortSerializer
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from djoser.views import UserViewSet as DjoserUserViewSet
from django.views.generic import ListView
from .mixins import CreateDeleteListViewSet
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from datetime import datetime
from django.http import HttpResponse

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from collections import Counter
from datetime import date

font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/fonts/arial.ttf')


# class UserViewSet(DjoserUserViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

class UserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:  # , 'me']:
            return UserCreateSerializer
        return CustomUserSerializer

    # @action(detail=False, methods=['get'])
    # def me(self, request, *args, **kwargs):
    #     serializer = UserSerializer(request.user)
    #     return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [AllowAny()]
    #     return super().get_permissions()

    # @action(detail=False, methods=['get'])
    # def me(self, request):
    #     serializer = self.get_serializer(request.user)
    #     return Response(serializer.data)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']

    # def list(self, request):
    #     tags = Tag.objects.all()
    #     serializer = TagSerializer(tags, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            raise NotFound(detail="Страница не найдена.")


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ingredient.DoesNotExist:
            raise NotFound(detail="Страница не найдена.")


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        return self.delete_from_shopping_cart(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Вы уже добавили рецепт в список покупок'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from_shopping_cart(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален или Вы не добавляли его в список покупок'},
                        status=status.HTTP_400_BAD_REQUEST)

    from django.db.models import Sum

    @action(detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        recipes = (
            ShoppingCart.objects
                .filter(user=user)
                .values('recipe__ingredients__name', 'recipe__ingredients__measurement_unit')
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


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
