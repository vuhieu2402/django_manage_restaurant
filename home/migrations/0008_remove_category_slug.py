# Generated by Django 4.2.15 on 2024-09-06 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
