# Generated by Django 2.2.1 on 2019-08-27 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain_mappings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainmapping',
            name='version',
            field=models.BigIntegerField(default=0),
        ),
    ]
