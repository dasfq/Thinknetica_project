# Generated by Django 3.2.3 on 2021-06-13 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0009_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='group',
            field=models.ManyToManyField(blank=True, related_name='users', to='auth.Group', verbose_name='Группа'),
        ),
    ]