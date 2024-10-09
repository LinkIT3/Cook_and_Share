# Generated by Django 5.1.1 on 2024-10-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_recipe_ingredient_quantity'),
        ('user', '0003_customuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='recipes_created',
        ),
        migrations.AddField(
            model_name='customuser',
            name='recipes_created',
            field=models.ManyToManyField(blank=True, db_index=True, null=True, related_name='author', to='recipe.recipe', verbose_name='Recipes created'),
        ),
    ]
