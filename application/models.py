from django.db import models
from django.contrib.auth.models import User
import uuid

from django.urls import reverse


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

    def get_absolute_url(self):
        return reverse('application:payment', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'


class Transaction(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    transaction_id = models.CharField(editable=False, null=True, max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    full_name = models.CharField(max_length=254, null=True)
    extra_data = models.TextField(null=True)
    payment_mode = models.CharField(max_length=200, default='CARD')
    is_successful = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f'{self.full_name}'


class Donation(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    ref_id = models.CharField(editable=False, max_length=8, unique=True,  default=generate_uuid())
    name = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    thumbnail = models.ImageField(upload_to='projects')
    amount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}'


class DonationUpdate(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='projects', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Donation updates'
        verbose_name_plural = 'Donation updates'

    def __str__(self):
        return f'{self.donation}'


class DonationComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(null=False)
    is_active = models.BooleanField('active', default=True,
                                    help_text='The project comment will still be visible to public.')
    added_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['added_on']
        verbose_name = 'Donation Comments'
        verbose_name_plural = 'Donation Comments'

    def __str__(self):
        return f'{self.comment}'

class DonationTransaction(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    transaction_id = models.CharField(editable=False, null=True, max_length=200)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    full_name = models.CharField(max_length=254, null=True)
    extra_data = models.TextField(null=True)
    payment_mode = models.CharField(max_length=200, default='CARD')
    is_successful = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f'{self.donation}'


class DonationIncentives(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    amount = models.IntegerField(default=0, null=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Donation Incentives'
        verbose_name_plural = 'Donation Incentives'

    def __str__(self):
        return f'{self.title}'

