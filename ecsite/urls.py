from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ec-index'),
    path('contact', views.contact, name='contact'),
    path('products', views.products, name='products'),
    path('product/<product_id>/', views.productDetail, name='product-detail'),
    path('category/<category_id>/', views.categoryDetails, name='category_products'),
    path('checkout', views.checkout, name='checkout'),
    path('orders', views.orders, name='orders'),
    path('order/create', views.create_order, name='create-order'),
    path('orders/<order_id>/', views.orderDetails, name='single_orders'),
    path('order/payment/', views.orderPesaPalPayment, name='order-payment'),
    path('payment/checkout/<order_id>', views.checkout, name='checkout'),
    path('order/payment/check', views.query_payment_status, name='order-payment-check'),
    path('comment/<product_id>/', views.productComment, name='product_comment'),
    # path('donations', views.Donations, name='donations'),
    # path('donation/<donation_id>', views.singleDonation, name='single-donation')
]
