# Generated by Django 3.0.4 on 2020-05-24 21:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ecsite', '0009_auto_20200525_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='public_id',
            field=models.UUIDField(default=uuid.UUID('fcf0bc82-6e29-438a-ab41-b9314f36ec62'), editable=False, primary_key=True, serialize=False),
        ),
    ]
