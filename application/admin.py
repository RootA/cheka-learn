from django.contrib import admin
from .models import Category, Project, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['category', 'ref_id', 'name', 'description', 'price', 'thumbnail', 'added_on', 'user']
    list_filter = ['category', 'user']
    # change_form_template = 'src/admin/project-create.html'

@admin.register(Transaction)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['project', 'full_name', 'amount', 'is_successful', 'transaction_date']
    list_filter = ['project', 'is_successful', 'full_name']
