# Generated by Django 3.0.4 on 2020-05-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20200510_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='ref_id',
            field=models.CharField(default='e6171bcd', editable=False, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='ref_id',
            field=models.CharField(default='60a69747', editable=False, max_length=8),
        ),
    ]