# Generated by Django 5.0.2 on 2024-02-22 09:57

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_comment_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None),
        ),
    ]