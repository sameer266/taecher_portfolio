# Generated by Django 5.2.1 on 2025-05-22 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_pdfbook_cover_image_pdfbook_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfbook',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.teacher'),
        ),
    ]
