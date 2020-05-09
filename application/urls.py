from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import DonationsView

urlpatterns = [
    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('project/<project_id>', views.project_detail, name='project-detail'),
    # path('project/<project_id>/process', views.project_checkout, name='project-detail'),
    path('project/payemnt/', views.payment_successful, name='payment-successful'),
    path('project/payment/check', views.query_payment_status, name='project-payment-check'),
    path('payment/<project_id>', views.project_checkout, name='payment'),
    
    path('donations', DonationsView.as_view(), name='donations'),
    path('donation/<str:donation_id>', views.singleDonation, name='donation'),
    path('donation/payment/<str:donation_id>', views.singleDonation, name='donation-payment')
]
