# Generated by Django 3.0.4 on 2020-05-02 12:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ecsite', '0004_auto_20200501_1746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitems',
            options={'ordering': ['-order_date'], 'verbose_name': 'Order Items', 'verbose_name_plural': 'Order Items'},
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='public_id',
            field=models.UUIDField(default=uuid.UUID('9c84ca82-b89d-43f3-97d3-59158d9df3e3'), editable=False, primary_key=True, serialize=False),
        ),
    ]
