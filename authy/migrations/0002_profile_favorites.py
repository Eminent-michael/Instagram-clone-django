# Generated by Django 3.2.15 on 2022-09-22 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20211016_1528'),
        ('authy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(to='post.Post'),
        ),
    ]