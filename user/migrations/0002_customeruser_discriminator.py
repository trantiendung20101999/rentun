# Generated by Django 3.2.5 on 2021-07-20 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='discriminator',
            field=models.CharField(default='', max_length=255),
        ),
    ]