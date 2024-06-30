# Generated by Django 3.2.25 on 2024-06-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_image'),
        ('tasks', '0003_alter_task_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_profiles',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='profiles.Profile'),
        ),
    ]