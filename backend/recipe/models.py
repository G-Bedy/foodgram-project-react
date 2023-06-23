from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django.core.validators import RegexValidator


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="название")
    # color = models.CharField(max_length=7, unique=True, verbose_name="цвет")  # HEX color code
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="цвет",
        validators=[
            RegexValidator(
                regex=r'^#[A-Fa-f0-9]{6}$',
                message="Цвет должен быть в формате HEX, например, '#E26C2D'."
            )
        ]
    )
    # slug = models.SlugField(max_length=200, unique=True, verbose_name="слаг")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message="Slug должен содержать только латинские буквы, цифры, дефисы и подчеркивания."
            )
        ]
    )
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.color})'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="название")
    measurement_unit = models.CharField(max_length=50, verbose_name="единица измерения")


    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'
        # return f'{self.name}'

    class Meta:
        unique_together = ('name', 'measurement_unit')
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class RecipeTag(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name="рецепт")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="тег")
    # quantity = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="количество")

    class Meta:
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецепта"


class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="автор")
    name = models.CharField(max_length=100, verbose_name="название")
    image = models.ImageField(upload_to='recipes/', verbose_name="изображение")
    text = models.TextField(verbose_name="описание")
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name="ингредиенты")
    tags = models.ManyToManyField(Tag, through=RecipeTag, verbose_name="теги")
    cooking_time = models.PositiveSmallIntegerField(verbose_name="время приготовления")  # in minutes

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="ингредиент")
    amount = models.PositiveSmallIntegerField(verbose_name="количество")

    def __str__(self):
        return self.ingredient.name

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"
