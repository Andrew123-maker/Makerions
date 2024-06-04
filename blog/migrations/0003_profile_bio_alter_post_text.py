# Generated by Django 5.0.2 on 2024-06-04 15:04

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_profile_bio_alter_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
