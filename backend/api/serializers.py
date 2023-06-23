import base64
from django.db.models import F
from django.core.files.base import ContentFile
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework import serializers
from users.models import CustomUser, Subscriber
from recipe.models import Tag, Ingredient, Recipe, RecipeIngredient
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields import fields as extra_fields

class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        return current_user.subscriber.filter(author=obj).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'id', 'username', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        extra_kwargs = {'slug': {'read_only': True}}

    # def to_representation(self, instance):
    #     return instance.title


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']



class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)
    # amount = IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = SerializerMethodField()
    author = UserCreateSerializer(many=False)
    image = extra_fields.Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipeingredient__amount')
        )
        return ingredients


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = RecipeIngredientSerializer(many=True)
    author = UserCreateSerializer(many=False, read_only=True)
    image = extra_fields.Base64ImageField(write_only=True)  # Используйте Base64ImageField из drf_extra_fields

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')

    def create_ingredients_amounts(self, ingredients, recipe):
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        image = validated_data.pop('image')
        current_user_id = self.context['request'].user.id

        tags_data = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        instance = Recipe.objects.create(author_id=current_user_id, image=image, **validated_data)
        instance.tags.set(tags_data)  # Добавление связанных тегов
        self.create_ingredients_amounts(recipe=instance,
                                        ingredients=ingredients)
        return instance

    # def create(self, validated_data):
    #     tags = validated_data.pop('tags')
    #     ingredients = validated_data.pop('ingredients')
    #
    #     recipe = Recipe.objects.create(**validated_data)
    #     recipe.tags.set(tags)
    #     self.create_ingredients_amounts(recipe=recipe,
    #                                     ingredients=ingredients)
    #     return recipe



    def update(self, instance, validated_data):
        # Обновление поля 'tags'
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        ingredients = validated_data.pop('ingredients')
        # Обновление поля 'ingredients'
        # if 'ingredients' in validated_data:
        #     ingredients_data = validated_data.pop('ingredients')
        #     # Перебираем данные об ингредиентах для обновления или создания новых ингредиентов
        #     for ingredient_data in ingredients_data:
        #         # Получаем или создаем ингредиент, используя 'id' для идентификации
        #         ingredient_id = ingredient_data.get('id', None)
        #         ingredient = RecipeIngredient.objects.get(pk=ingredient_id) if ingredient_id else None
        #         ingredient_serializer = RecipeIngredientSerializer(ingredient, data=ingredient_data)
        #         if ingredient_serializer.is_valid():
        #             ingredient_serializer.save(recipe=instance)

        # Обновление остальных полей
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)

        # Обновление поля 'image'
        if 'image' in validated_data:
            instance.image = validated_data['image']

        instance.save()
        return instance

    # def get_ingredients(self, obj):
    #     ingredients = obj.ingredients.all()
    #     serialized_ingredients = []
    #     for ingredient in ingredients:
    #         serialized_ingredient = {
    #             'id': ingredient.id,
    #             'amount': ingredient.amount
    #         }
    #         serialized_ingredients.append(serialized_ingredient)
    #     return serialized_ingredients

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance,
                                context=context).data


class SubscriberSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Subscriber
        fields = ['user', 'author']
