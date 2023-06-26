from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from djoser.views import UserViewSet as DjoserUserViewSet
# from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from django.views.generic import ListView
# from .mixins import CreateDeleteListViewSet
from rest_framework.viewsets import ModelViewSet, ViewSet

# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.exceptions import NotFound
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.exceptions import NotFound
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from django.views.decorators.http import require_http_methods
# from django.db.models import Sum
# from datetime import datetime
# from django.http import HttpResponse
from api.pagination import CustomPagination
# from recipe.models import Tag, Ingredient, Recipe, ShoppingCart, RecipeIngredient, Favorite
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeCreateSerializer,
                             RecipeIngredientSerializer, RecipeSerializer,
                             RecipeShortSerializer, SubscribeSerializer,
                             TagSerializer, UserCreateSerializer)
# from rest_framework.response import Response
from users.models import CustomUser, Subscribe

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(CustomUser, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(author,
                                             data=request.data,
                                             context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(Subscribe,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)

