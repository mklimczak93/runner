# Generated by Django 4.1.7 on 2023-04-26 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default='bio', max_length=280),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='user_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default='network/static/User01.png', upload_to='user_profiles'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=280)),
                ('date', models.DateField(default=1993)),
                ('photo', models.ImageField(default='network/static/post_01.jpg', upload_to='images_uploaded')),
                ('liked_by', models.ManyToManyField(blank=True, related_name='upvoter', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
