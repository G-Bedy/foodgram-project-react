from django.contrib import admin
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline, RecipeTagInline,)

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(_favorite_count=models.Count('favorite', distinct=True))
    #     return queryset

    # def favorite_count(self, obj):
    #     return obj._favorite_count

    # favorite_count.short_description = 'Number of times added to favorites'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    # list_display = ('recipe', 'ingredient', 'quantity')
    list_display = ('recipe', 'ingredient', 'quantity_with_unit')

    def quantity_with_unit(self, obj):
        return f'{int(obj.amount)} {obj.ingredient.measurement_unit} (а/ов)'
    quantity_with_unit.short_description = 'Количество (ед. изм.)'
