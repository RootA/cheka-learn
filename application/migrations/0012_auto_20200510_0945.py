# Generated by Django 3.0.4 on 2020-05-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_auto_20200509_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='ref_id',
            field=models.CharField(default='7dee7fdc', editable=False, max_length=8),
        ),
        migrations.AlterField(
            model_name='project',
            name='ref_id',
            field=models.CharField(default='01ad1705', editable=False, max_length=8),
        ),
    ]
