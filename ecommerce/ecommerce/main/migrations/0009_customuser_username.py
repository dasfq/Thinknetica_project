# Generated by Django 3.2.3 on 2021-06-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210612_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Логин'),
        ),
    ]