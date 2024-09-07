# Generated by Django 5.1.1 on 2024-09-07 15:28

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, verbose_name='Слаг')),
                ('image', models.ImageField(blank=True, upload_to='images/categories', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'default_related_name': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, verbose_name='Слаг')),
                ('thumbnail', models.ImageField(blank=True, upload_to='images/thumbnails', verbose_name='Превью')),
                ('medium_image', models.ImageField(blank=True, upload_to='images/medium', verbose_name='Изображение среднего размера')),
                ('large_image', models.ImageField(blank=True, upload_to='images/large', verbose_name='Изображение большого размера')),
                ('price', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)], verbose_name='Цена продукта')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='Категория продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'default_related_name': 'products',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Продукты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'default_related_name': 'shopping_cart',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, verbose_name='Слаг')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.subcategory', verbose_name='Подкатегория продукта'),
        ),
    ]
