# Generated by Django 3.2.15 on 2022-10-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_alter_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=75, unique=True, verbose_name='Tag'),
        ),
    ]
