# Generated by Django 2.1.2 on 2018-10-15 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='author',
            new_name='user',
        ),
    ]
