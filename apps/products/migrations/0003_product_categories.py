# Generated by Django 4.2.11 on 2024-04-19 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_category_options_alter_review_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='products.category'),
        ),
    ]