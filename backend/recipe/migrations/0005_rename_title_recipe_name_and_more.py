# Generated by Django 4.2.2 on 2023-06-21 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_alter_recipeingredient_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
    ]
