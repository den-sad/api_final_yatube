# Generated by Django 3.2.16 on 2023-02-14 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230214_1102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]
