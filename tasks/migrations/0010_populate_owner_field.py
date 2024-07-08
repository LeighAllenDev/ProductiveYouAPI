from django.db import migrations, models

def set_default_owner(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    User = apps.get_model('auth', 'User')
    default_user = User.objects.first()
    for task in Task.objects.filter(owner__isnull=True):
        task.owner = default_user
        task.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_task_owner'),
    ]

    operations = [
        migrations.RunPython(set_default_owner),
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='tasks', to='auth.User'),
        ),
    ]
