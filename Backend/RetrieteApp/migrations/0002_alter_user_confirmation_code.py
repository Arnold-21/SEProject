# Generated by Django 4.1.7 on 2023-05-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RetrieteApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
