from django.db import models
from currencies.models import Currency
import uuid


class Category(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(default='default.png')
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('active', default=True,
                                    help_text='The category will be available.')

    class Meta:
        ordering = ['name']
        verbose_name = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


def singleItem(product_id):
    product = Item.objects.filter(public_id=product_id).first()
    images = Image.objects.filter(item=product_id).all()
    categories = Category.objects.all()
    comments = Comments.objects.filter(item_id=product_id).all()
    context = {
        'product': product,
        'images': images,
        'categories': categories,
        'comments': comments
    }
    return context


class Item(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)  # Usually a percentage
    image = models.FileField()
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('active', default=True,
                                    help_text='The item will be available.')

    def __str__(self):
        return self.name

    @property
    def thumbnail_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Image(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='+')
    upload = models.FileField()
    is_active = models.BooleanField('active', default=True,
                                    help_text='The image will be available.')


class Order(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    buyer_name = models.CharField(max_length=200)
    buyer_email = models.EmailField(null=True)
    buyer_phone_address = models.CharField(max_length=20, null=True)
    buyer_address = models.TextField(null=True)
    discounted = models.IntegerField(default=0)  # means no discount to be applied
    order_date = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=254, null=True, unique=True, db_index=True)
    ref_id = models.CharField(max_length=254, null=True, unique=True, db_index=True)
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.buyer_name

class OrderItems(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Order Items'
        verbose_name_plural = 'Order Items'


class ProcessingStages(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'processing_stages'
        verbose_name_plural = 'processing_stages'


class OrderStage(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stage = models.ForeignKey(ProcessingStages, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return {self.order, self.stage}


class Comments(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(null=False)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item


class Project(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    thumbnail = models.FileField()
    is_active = models.BooleanField('active', default=True,
                                    help_text='The project will still be available.')
    added_on = models.DateTimeField(auto_now=True)
    seed_money = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']
        verbose_name = 'projects'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.name

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url


class ProjectSeed(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    amount = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['project_id']
        verbose_name = 'project_seeds'
        verbose_name_plural = 'project_seeds'


class ProjectComment(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(null=False)
    is_active = models.BooleanField('active', default=True,
                                    help_text='The project comment will still be visible to public.')
    added_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['project_id']
        verbose_name = 'project_comments'
        verbose_name_plural = 'project_comments'


class ProjectUpdate(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    thumbnail = models.FileField(null=True)
    is_active = models.BooleanField('active', default=True,
                                    help_text='The project update will still be available.')
    added_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['project_id']
        verbose_name = 'project_updates'
        verbose_name_plural = 'project_updates'

    def __str__(self):
        return self.project_id


class ProjectImage(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.FileField(null=True)

    class Meta:
        ordering = ['project_id']
        verbose_name = 'project_images'
        verbose_name_plural = 'project_images'
