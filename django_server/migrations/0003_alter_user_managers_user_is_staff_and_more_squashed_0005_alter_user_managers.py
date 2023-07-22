# Generated by Django 4.2.3 on 2023-07-22 17:51

from django.db import migrations, models
import django_server.models


class Migration(migrations.Migration):

    replaces = [('django_server', '0003_alter_user_managers_user_is_staff_and_more'), ('django_server', '0004_alter_user_managers'), ('django_server', '0005_alter_user_managers')]

    dependencies = [
        ('django_server', '0002_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django_server.models.GoogleUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django_server.models.GoogleUserManager()),
            ],
        ),
    ]
