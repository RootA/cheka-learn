from django.contrib import admin

from .models import Category, Item, Order, Image, ProcessingStages, OrderStage, \
    Project, ProjectImage, ProjectSeed, \
    ProjectUpdate, ProjectComment, OrderItems

admin.site.site_header = "CHEKATV DASHBOARD"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'is_active')


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'description', 'price', 'discount', 'is_active', 'image', 'created_at')
    list_filter = ['category']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'ref_id', 'transaction_id', 'buyer_address',
                    'discounted', 'amount','is_paid', 'order_date')
    list_filter = ['is_paid', 'buyer_phone_address', 'discounted']

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price', 'order_date')
    list_filter = ['order', 'item']

class ImagesAdmin(admin.ModelAdmin):
    list_display = ('item', 'upload')
    list_filter = ['item']


class ProcessingStagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class OrderStageAdmin(admin.ModelAdmin):
    list_display = ('order', 'stage', 'is_done', 'added_on')
    list_filter = ['order', 'stage']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'thumbnail', 'is_active', 'seed_money', 'added_on')


class ProjectSeedAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'full_name', 'email', 'amount', 'added_on')
    list_filter = ['project_id']


class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'description', 'thumbnail', 'is_active')
    list_filter = ['project_id']


class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'image')
    list_filter = ['project_id']


class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'comment', 'full_name', 'is_active', 'added_on')
    list_filter = ['project_id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemsAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(Image, ImagesAdmin)
admin.site.register(ProcessingStages, ProcessingStagesAdmin)
admin.site.register(OrderStage, OrderStageAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectSeed, ProjectSeedAdmin)
admin.site.register(ProjectImage, ProjectImageAdmin)
admin.site.register(ProjectUpdate, ProjectUpdateAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)

