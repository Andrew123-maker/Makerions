# Generated by Django 5.0.2 on 2024-06-03 16:21

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]