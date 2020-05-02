from django.shortcuts import render

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Sum, Count
from django.contrib import messages
from django.http import JsonResponse

from .models import Category, Item, Comments, Project, ProjectSeed, ProjectComment, Order, OrderItems
from .models import singleItem
from .utility_functions import Mail, Helpers

from application.payment import postDirectOrder, queryPaymentDetails
import json
import uuid


def index(request):
    all_products = Item.objects.all()
    context = {
        'title': 'CHEKA TV',
        'products': all_products,
        'categories': Helpers.fetchCategories()
    }
    return render(request, 'src/ecom/index.html', context)


def contact(request):
    context = {
        'title': 'CHEKA TV - Contact',
        'categories': Helpers.fetchCategories()
    }
    return render(request, 'src/ecom/contact.html', context)


def contactRequest(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        new_mail = Mail()
        new_mail.sendMail(full_name, email, subject, message)
    return render(request, 'src/ecom/contact.html')


def categoryDetails(request, category_id):
    category_products = Item.objects.filter(category_id=category_id).all()
    category = Category.objects.filter(pk=category_id).first()
    context = {
        'products': category_products,
        'categories': Helpers.fetchCategories(),
        'category': category,
        'key_text': category.name,
        'title': category.name
    }
    return render(request, 'src/ecom/products.html', context)


def products(request):
    all_products = Item.objects.all()
    context = {
        'title': 'CHEKA TV - Products',
        'products': all_products,
        'categories': Helpers.fetchCategories()
    }
    return render(request, 'src/ecom/products.html', context)


def productDetail(request, product_id):
    context = singleItem(product_id)
    return render(request, 'src/ecom/product.html', context)


def productComment(request, product_id):
    if request.method == 'POST':
        obj = Comments()
        obj.full_name = request.POST.get('name')
        obj.email = request.POST.get('email')
        obj.comment = request.POST.get('comment')
        obj.item_id = product_id
        obj.save()
    context = singleItem(product_id)
    return render(request, 'src/ecom/product.html', context)

def create_order(request):
    FirstName = request.POST.get('FirstName')
    LastName = request.POST.get('LastName')
    Email = request.POST.get('Email')
    Amount = request.POST.get('Amount')
    order_id = uuid.uuid4()
    ref_id = str(order_id)[:8]
    new_order = Order.objects.create(
        public_id=order_id,
        ref_id=ref_id,
        buyer_name=f'{FirstName} {LastName}',
        buyer_email=Email
    )
    order_items = json.loads(request.POST.get('cart'))
    for item in order_items:
        item_ = Item.objects.get(pk=item['itemId'])
        OrderItems.objects.create(
            public_id=uuid.uuid4(),
            order=new_order,
            quantity=item['count'],
            price=item['price'],
            item=item_
        )

    request_data = {
        'Amount': str(int(Amount)),
        'Currency': 'USD',
        'Description': 'Order checkout',
        'Type': 'MERCHANT',
        'Reference': ref_id,
        'FirstName': FirstName,
        'LastName': LastName,
        'Email': Email,
    }
    post_params = {
        'oauth_callback': f'http://localhost:8000/order/payment/'
    }
    # build url to redirect user to confirm payment
    url = postDirectOrder(post_params, request_data)
    context = {
        'url': url,
        'title': 'Checkout'
    }
    return JsonResponse(context)
    # return HttpResponse(json.dumps(context), content_type='application/json')
    # return render(request, 'src/checkout.html', context)

def orderPesaPalPayment(request):
    order = Order.objects.get(pk=request.get('pesapal_merchant_reference'))
    order.transaction_id = request.get('pesapal_transaction_tracking_id')
    order.save()
    context = {
        'title': 'Check Payment',
        'transaction_id': request.get('pesapal_transaction_tracking_id'),
        'show_success': False,
    }
    return render(request, 'src/confirm.html', context)

def query_payment_status(request):
    transaction_id = request.POST.get('transaction_id')
    order = Order.objects.filter(transaction_id=transaction_id).first()
    params = {
        'pesapal_merchant_reference': order.pk,
        'pesapal_transaction_tracking_id': transaction_id
    }

    status = queryPaymentDetails(params)
    if status.split(',')[2] == 'COMPLETED':
        order.is_paid = True
        order.save()
        return render(request, 'src/success.html')
    elif status.split(',')[2] == 'PENDING':
        context = {
            'title': 'Check Payment',
            'transaction_id': transaction_id,
            'show_success': False,
        }
        return render(request, 'src/confirm.html', context)
    elif status.split(',')[2] == 'FAILED':
        order.is_paid = False
        order.save()
        return render(request, 'src/failure.html')
    else:  # INVALID
        order.is_paid = False
        order.save()
        return render(request, 'src/failure.html')

def checkout(request):
    return HttpResponse("Viewing the checkout page")


def orders(request):
    return HttpResponse("Viewing all orders")


def orderDetails(request, order_id):
    return HttpResponse("Viewing order %s" % order_id)


def payments(request):
    return HttpResponse("Viewing all payments")


def Donations(request):
    donations = Project.objects.filter(is_active=True).all()
    paginator = Paginator(donations, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list_pages = []
    if page_obj.paginator.num_pages > 0:
        for page in range(0, page_obj.paginator.num_pages):
            list_pages.append(page + 1)
    context = {
        'title': 'Cheka Tv - Donations',
        'donations': page_obj,
        'page_obj': page_obj,
        'list_pages': list_pages,
        'categories': Helpers.fetchCategories()
    }
    return render(request, 'src/ecom/donations.html', context)


def singleDonation(request, donation_id):
    donation = Project.objects.get(public_id=donation_id)
    seeds = ProjectSeed.objects.filter(project_id=donation_id).aggregate(Sum('amount'))
    comments = ProjectComment.objects.filter(project_id=donation_id, is_active=True).all()
    context = {
        'donation': donation,
        'seeds': seeds,
        'comments': comments,
        'categories': Helpers.fetchCategories()
    }
    return render(request, 'src/ecom/single-donation.html', context)