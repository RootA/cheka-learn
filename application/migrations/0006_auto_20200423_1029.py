# Generated by Django 3.0.4 on 2020-04-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_auto_20200422_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ref_id',
            field=models.CharField(default='bd278a71', editable=False, max_length=8),
        ),
    ]