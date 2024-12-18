# Generated by Django 4.2.15 on 2024-09-10 11:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_alter_recipe_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='name',
        ),
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(default=str, max_length=300, validators=[django.core.validators.MinLengthValidator(10)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='title',
            field=models.TextField(db_index=True, default=str, max_length=100, validators=[django.core.validators.MinLengthValidator(2)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(max_length=50000, validators=[django.core.validators.MinLengthValidator(100)]),
        ),
    ]
