# Generated by Django 3.0.4 on 2020-04-22 09:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20200422_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d7b3fc2b-2862-4ad2-9f8a-ca2551d92fec'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.UUIDField(default=uuid.UUID('243ae14b-99dd-47f5-a3d2-778421f674b2'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='ref_id',
            field=models.CharField(default=uuid.UUID('5b3e744d-2f25-4bdd-9905-f745d3d2b471'), editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1052340c-d4c2-4ff5-90c7-bd820f09acc0'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('bc15e50a-7c12-4f31-b2b2-fc829b678a11'), editable=False, max_length=10),
        ),
    ]
