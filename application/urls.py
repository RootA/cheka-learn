from django.urls import path
from . import views
from .views import DonationsView, CommentView

urlpatterns = [
    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('project/<project_id>', views.project_detail, name='project-detail'),
    # path('project/<project_id>/process', views.project_checkout, name='project-detail'),
    path('project/payment/', views.payment_successful, name='payment-successful'),
    path('project/payment/check', views.query_payment_status, name='project-payment-check'),
    path('payment/<project_id>', views.project_checkout, name='payment'),

    path('donations', DonationsView.as_view(), name='donations'),
    path('donation/<str:donation_id>', views.singleDonation, name='donation'),
    path('donation/comment/<str:donation_id>', CommentView.as_view(), name='comment'),
    path('donation/payment/<str:donation_id>', views.donationPayment, name='donation-payment'),
    path('donation/payment/callback', views.donationPaymentCallback, name='donation-payment-callback'),

    path('payment/paypal/transaction', views.paypal_checkout_success, name='paypal-success')
]
