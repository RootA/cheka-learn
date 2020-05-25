from django.contrib import admin
from .models import Category, Project, Transaction, Donation, DonationUpdate, DonationTransaction, DonationComment, \
                    DonationIncentives, Schedule, ProjectSchedule, ProjectDays, ProjectBookings

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['category', 'ref_id', 'name', 'description', 'price', 'thumbnail', 'added_on', 'user']
    list_filter = ['category', 'user']
    # change_form_template = 'src/admin/project-create.html'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'time_start', 'duration', 'is_active']
    list_filter = ['is_active']

@admin.register(ProjectSchedule)
class ProjectScheduleAdmin(admin.ModelAdmin):
    list_display = ['project', 'schedule', 'is_active']
    list_filter = ['project', 'schedule']

@admin.register(ProjectDays)
class ProjectScheduleAdmin(admin.ModelAdmin):
    list_display = ['project', 'day']
    list_filter = ['project', 'day']


@admin.register(ProjectBookings)
class ProjectBookingsAdmin(admin.ModelAdmin):
    list_display = ['project', 'full_name', 'date', 'schedule', 'email', 'added_on', 'is_paid']
    list_filter = ['project', 'date']

@admin.register(Transaction)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['project', 'transaction_id', 'full_name', 'amount', 'is_successful', 'transaction_date']
    list_filter = ['project', 'is_successful', 'full_name']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['ref_id', 'name', 'description', 'amount', 'is_active', 'created_at']
    list_filter = ['is_active']

@admin.register(DonationUpdate)
class DonationUpdateAdmin(admin.ModelAdmin):
    list_display = ['donation', 'description', 'created_at']
    list_filter = ['donation']

@admin.register(DonationComment)
class DonationCommentAdmin(admin.ModelAdmin):
    list_display = ['donation', 'comment', 'full_name', 'added_on']
    list_filter = ['donation']

@admin.register(DonationTransaction)
class DonationTransactionAdmin(admin.ModelAdmin):
    list_display = ['donation', 'full_name', 'amount', 'is_successful', 'transaction_date']
    list_filter = ['donation', 'is_successful', 'full_name']\

@admin.register(DonationIncentives)
class DonationIncentivesAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'is_active', 'created_at']
