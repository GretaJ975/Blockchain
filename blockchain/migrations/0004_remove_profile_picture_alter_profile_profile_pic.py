# Generated by Django 5.1.7 on 2025-04-05 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0003_profile_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='blockchain/profile_pics/default.png', null=True, upload_to='blockchain/profile_pics/'),
        ),
    ]
