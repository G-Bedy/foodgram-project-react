from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from slugify import slugify
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator

CustomUser = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name="название"
    )
    color = ColorField(
        unique=True,
        verbose_name="цвет"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message="Slug должен содержать только латинские буквы, "
                        "цифры, дефисы и подчеркивания."
            )
        ]
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f'{self.name} ({self.color})'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="название"
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name="единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name="рецепт"
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name="тег"
    )

    class Meta:
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецепта"


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="автор",
        related_name='recipes'
    )
    name = models.CharField(
        max_length=100,
        verbose_name="название",
        blank=False
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name="изображение",
        blank=False
    )
    text = models.TextField(verbose_name="описание", blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name="ингредиенты",
        related_name='recipes',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        through=RecipeTag,
        verbose_name="теги"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="время приготовления",
        help_text="Введите время приготовления в минутах.",
        validators=[
            MinValueValidator(1, message="Время приготовления должно быть больше 0.")
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="ингредиент"
    )
    amount = models.PositiveSmallIntegerField(verbose_name="количество")

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"

    def __str__(self):
        return self.ingredient.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name="рецепты"
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f"Список покупок для пользователя {self.user.username}"


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name="пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name="Рецепты"
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favourite')
        ]
