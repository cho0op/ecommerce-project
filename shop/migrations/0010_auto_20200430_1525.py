# Generated by Django 3.0.5 on 2020-04-30 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200430_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desctiption',
            new_name='description',
        ),
    ]
