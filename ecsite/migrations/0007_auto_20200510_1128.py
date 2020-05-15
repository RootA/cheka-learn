# Generated by Django 3.0.4 on 2020-05-10 11:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ecsite', '0006_auto_20200502_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='public_id',
            field=models.UUIDField(default=uuid.UUID('4ddc511f-2676-45fe-91e1-2f817fe2e5f6'), editable=False, primary_key=True, serialize=False),
        ),
    ]