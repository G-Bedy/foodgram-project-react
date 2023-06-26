# Generated by Django 4.2.2 on 2023-06-20 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipe', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                through='recipe.RecipeIngredient', to='recipe.ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                through='recipe.RecipeTag', to='recipe.tag', verbose_name='теги'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together={('name', 'measurement_unit')},
        ),
    ]
