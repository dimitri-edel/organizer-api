# Generated by Django 3.2.20 on 2023-10-15 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_chat', '0002_alter_teammessage_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teammessage',
            old_name='task',
            new_name='team',
        ),
    ]