# Generated by Django 4.2 on 2023-06-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200, verbose_name='пароль'),
        ),
    ]
