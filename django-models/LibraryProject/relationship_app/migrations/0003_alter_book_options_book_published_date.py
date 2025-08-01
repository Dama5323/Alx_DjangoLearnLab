# Generated by Django 5.2.4 on 2025-07-17 21:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('can_add_book', 'Can add book'), ('can_change_book', 'Can change book'), ('can_delete_book', 'Can delete book')]},
        ),
        migrations.AddField(
            model_name='book',
            name='published_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
