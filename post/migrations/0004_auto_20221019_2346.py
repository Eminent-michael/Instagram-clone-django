# Generated by Django 3.2.15 on 2022-10-19 23:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0003_auto_20211016_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='caption',
        ),
        migrations.CreateModel(
            name='PostFileContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=post.models.user_directory_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.ManyToManyField(related_name='contents', to='post.PostFileContent'),
        ),
    ]
