from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser, Subscriber
from recipe.models import Tag, Ingredient, Recipe
from .serializers import UserCreateSerializer, TagSerializer, IngredientSerializer, \
    RecipeSerializer, RecipeCreateSerializer, RecipeIngredientSerializer, SubscriberSerializer, \
    CustomUserSerializer
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


# class UserViewSet(DjoserUserViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

class UserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']: #, 'me']:
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


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer



# class TagViewSet(viewsets.ModelViewSet):
# class TagViewSet(ListView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
    # permission_classes = (AdminOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)
    # lookup_field = 'slug'

# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from users.models import CustomUser
# from .serializers import UserSerializer
# from djoser.views import UserViewSet

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_permissions(self):
#         if self.action == 'create':
#             return [AllowAny()]
#         return [IsAuthenticated()]
#
#     @action(detail=False, methods=['get'])
#     def me(self, request):
#         serializer = self.get_serializer(request.user)
#         return Response(serializer.data)
