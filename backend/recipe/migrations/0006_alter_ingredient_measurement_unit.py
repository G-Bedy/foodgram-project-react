# Generated by Django 4.2.2 on 2023-06-23 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_rename_title_recipe_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=50, verbose_name='единица измерения'),
        ),
    ]