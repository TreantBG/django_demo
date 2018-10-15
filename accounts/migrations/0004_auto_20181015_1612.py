# Generated by Django 2.1.2 on 2018-10-15 13:12

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_cart'),
        ('accounts', '0003_auto_20181015_1405'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cart',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Cart', verbose_name='Cart'),
        ),
    ]