# Generated by Django 3.2.3 on 2021-06-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210601_0106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketcar',
            options={'ordering': ('-date_modified',), 'verbose_name': 'Объявление - авто', 'verbose_name_plural': 'Объявления - авто'},
        ),
        migrations.AlterModelOptions(
            name='ticketitem',
            options={'ordering': ('-date_modified',), 'verbose_name': 'Объявление - вещи', 'verbose_name_plural': 'Объявления - вещи'},
        ),
        migrations.AlterModelOptions(
            name='ticketservice',
            options={'ordering': ('-date_modified',), 'verbose_name': 'Объявление - услуги', 'verbose_name_plural': 'Объявления - услуги'},
        ),
        migrations.AlterField(
            model_name='ticketcar',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticketcar',
            name='name',
            field=models.CharField(max_length=25, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='ticketitem',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticketitem',
            name='name',
            field=models.CharField(max_length=25, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='ticketservice',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticketservice',
            name='name',
            field=models.CharField(max_length=25, verbose_name='Название'),
        ),
    ]
