# Generated by Django 3.0.4 on 2020-04-22 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('0c4d8292-2999-4193-a55a-564647943a67'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Categories',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('63995f0a-74d6-4f8f-83a5-1365afb95995'), editable=False, primary_key=True, serialize=False)),
                ('ref_id', models.CharField(default=uuid.UUID('3eac6329-decf-4ebb-8924-d6785973ece8'), editable=False, max_length=10)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thumbnail', models.ImageField(upload_to='projects')),
                ('is_active', models.BooleanField(default=True)),
                ('added_on', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('32ec5942-eabd-42ea-871a-31da8edb47fa'), editable=False, primary_key=True, serialize=False)),
                ('transaction_id', models.CharField(default=uuid.UUID('9be3c051-2635-420c-8961-8c8e08c434db'), editable=False, max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('full_name', models.CharField(max_length=254)),
                ('extra_data', models.TextField()),
                ('payment_mode', models.CharField(default='CARD', max_length=200)),
                ('is_successful', models.BooleanField(default=False)),
                ('transaction_date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Project')),
            ],
            options={
                'ordering': ['-transaction_date'],
            },
        ),
    ]
