# Generated by Django 2.0 on 2018-06-05 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djconnectwise', '0060_auto_20180605_0840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('name', 'id'), 'verbose_name_plural': 'Teams'},
        ),
    ]