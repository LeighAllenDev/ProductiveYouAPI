# Generated by Django 3.2.25 on 2024-06-30 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_alter_team_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='members',
            new_name='users',
        ),
    ]
