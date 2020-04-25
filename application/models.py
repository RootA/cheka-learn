from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_uuid():
    return str(uuid.uuid4())[:8]

class Category(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=False)

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

class Project(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    ref_id = models.CharField(editable=False, default=generate_uuid(), max_length=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='projects')
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Transaction(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    transaction_id = models.CharField(editable=False, null=True, max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    full_name = models.CharField(max_length=254)
    extra_data = models.TextField()
    payment_mode = models.CharField(max_length=200, default='CARD')
    is_successful = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f'{self.full_name}'
