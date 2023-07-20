# Generated by Django 4.2.3 on 2023-07-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('release_date', models.DateField(verbose_name='Дата выхода')),
                ('lte_exists', models.BooleanField(default=True, verbose_name='Наличие LTE')),
                ('slug', models.SlugField(max_length=255)),
            ],
        ),
    ]
