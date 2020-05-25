from datetime import datetime
from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView

from .models import *
from collections import Counter

from ecsite.models import Order, Item, OrderItems
from .utility_functions import *
from .forms import CommentForm

import requests
import json

from .payment import postDirectOrder, queryPaymentDetails


def index(request):
    context = {
        'hero_text': 'KARIBU',
        'key_text': 'CHEKA オンライン',
        'summary': '"アフリカの笑顔と日本を繋ぐ"',
        'thumbnail': '/img/chekafe Logo.png',
        'thumbnail1': '/img/ChekaTV.jpg',
        'thumbnail2': '/img/CHEKAIZAKAYALOGO.jpg',
        'title': 'Cheka'
    }
    return render(request, 'src/index.html', context)


def projects(request):
    categories = fetch_categories()
    all_projects = fetch_projects()

    context = {
        'categories': categories,
        'projects': all_projects,
        'hero_text': 'Lets connect online with different activities, through',
        'key_text': 'Cheka チェカTV',
        'summary': '"アフリカの笑顔と日本を繋ぐ"',
        'thumbnail': '/img/chekafe Logo.png',
        'thumbnail1': '/img/ChekaTV.jpg',
        'thumbnail2': '/img/CHEKAIZAKAYALOGO.jpg',
        'title': 'Cheka projects'
    }
    return render(request, 'src/projects.html', context)

def project_detail(request, project_id):
    categories = fetch_categories()
    project = fetch_single_project(project_id)
    schedules = [schedule for schedule in ProjectSchedule.objects.filter(project=project).all()]
    okayDays = []
    okayDaysInt = None
    acceptedDays = []
    for day in ProjectDays.objects.filter(project__exact=project).all():
        acceptedDays.append(day.get_id())
        okayDays.append(day)
        if okayDaysInt is None:
            okayDaysInt = f'{day.get_id()}'
        else:
            okayDaysInt = f'{okayDaysInt}, {day.get_id()}'
    days = [0, 1, 2, 3, 4, 5, 6, 7]
    main_list = list(set(days) - set(acceptedDays))
    disableddays = listToString(main_list)
    context = {
        'categories': categories,
        'project': project,
        'key_text': project.name,
        'summary': f'${project.price}',
        'checkout_amount': int(project.price * 100),
        'thumbnail': '/img/chekafe Logo.png',
        'thumbnail1': '/img/ChekaTV.jpg',
        'thumbnail2': '/img/CHEKAIZAKAYALOGO.jpg',
        'title': project.name,
        'schedules': schedules,
        'okayDays': okayDays,
        'okayDaysInt': okayDaysInt,
        'disAbledDays': disableddays
    }

    return render(request, 'src/detail.html', context)



# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = None

    for element in s:
        if str1:
            str1 = f'{str1},{element}'
        else:
            str1 = f'{element}'

    # return string
    return str1

def project_checkout(request, project_id):
    project = fetch_single_project(project_id)
    schedule = ProjectSchedule.objects.get(pk=request.POST.get('session'))
    booking = ProjectBookings.objects.create(
        project=project,
        date=request.POST.get('date'),
        full_name=f'{request.POST.get("first_name")} {request.POST.get("last_name")}',
        email=request.POST.get('email'),
        schedule=schedule
    )
    context = {
        'url': 'http://localhost:8000/project/payment',
        'Amount': str(int(project.price)),
        'Currency': 'USD',
        'summary': f'${project.price}',
        'key_text': project.name,
        'project': project,
        'Reference': booking.pk,
        'type': 1,
        'title': 'Checkout'
    }
    return render(request, 'src/checkout.html', context)

class DonationsView(ListView):
    model = Donation
    template_name = 'src/donations.html'
    context_object_name = 'donations'

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).all()


def singleDonation(request, donation_id):
    donation = Donation.objects.get(id=donation_id)
    donation_updates = DonationUpdate.objects.filter(donation=donation, is_active=True)
    seeds = DonationTransaction.objects.filter(donation=donation).all()
    comments = DonationComment.objects.filter(donation=donation, is_active=True).all().reverse()
    incentives = DonationIncentives.objects.filter(is_active=True).all().reverse()
    form = CommentForm()
    context = {
        'donation': donation,
        'seeds': seeds,
        'comments': comments,
        'incentives': incentives,
        'updates': donation_updates,
        'comment_form': form
    }
    return render(request, 'src/single_donation.html', context)


def donationPayment(request, donation_id):
    amount = request.POST.get('amount')
    firstName = request.POST.get('first_name')
    lastName = request.POST.get('last_name')
    Email = request.POST.get('email')
    donation = Donation.objects.get(id=donation_id)
    incentive = DonationIncentives.objects.get(pk=amount)
    transaction = DonationTransaction.objects.create(
        donation=donation,
        full_name=f'{firstName} {lastName}',
        amount=incentive.amount
    )

    request_data = {
        'Amount': str(int(incentive.amount)),
        'Currency': 'USD',
        'Description': donation.name,
        'Type': 'MERCHANT',
        'Reference': transaction.pk,
        'FirstName': firstName,
        'LastName': lastName,
        'Email': Email,
        'type': 3
    }

    return render(request, 'src/checkout.html', request_data)

def donationPaymentCallback(request):
    ref_id = request.get('pesapal_merchant_reference')
    transaction_id = request.get('pesapal_transaction_tracking_id')
    donation = Donation.objects.filter(ref_id=ref_id).first()
    if donation:
        donation.transaction_id = transaction_id
        donation.save()

    context = {
        'title': 'Check Payment',
        'transaction_id': transaction_id,
        'show_success': False,
    }
    return render(request, 'src/check_transaction.html', context)

class CommentView(FormView):
    model = DonationComment
    form_class = CommentForm()

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            donation = Donation.objects.get(id=kwargs['donation_id'])
            form.instance.donation = donation
            form.save()
            messages.info(request, 'Thank you for the comment!')
            return redirect('donation', donation.pk)
        else:
            return self.form_invalid(form)


def pesapal_callback(request):
    ref_id = request.get('pesapal_merchant_reference')
    transaction_id = request.get('pesapal_transaction_tracking_id')
    project = Project.objects.filter(ref_id=ref_id).first()
    if project:
        Transaction.objects.create(
            transaction_id=transaction_id,
            project=project,
            payment_mode='CARD',
        )

    context = {
        'title': 'Check Payment',
        'transaction_id': transaction_id,
        'show_success': False,
    }
    return render(request, 'src/check_transaction.html', context)


def query_payment_status(request):
    transaction_id = request.POST.get('transaction_id')
    transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
    params = {
        'pesapal_merchant_reference': transaction.project.ref_id,
        'pesapal_transaction_tracking_id': transaction_id
    }

    status = queryPaymentDetails(params)
    if status.split(',')[2] == 'COMPLETED':
        transaction.is_successful = True
        transaction.save()
        return render(request, 'src/success.html')
    elif status.split(',')[2] == 'PENDING':
        context = {
            'title': 'Check Payment',
            'transaction_id': '1212',
            'show_success': False,
        }
        return render(request, 'src/check_transaction.html', context)
    elif status.split(',')[2] == 'FAILED':
        transaction.is_successful = False
        transaction.save()
        return render(request, 'src/failure.html')
    else:  # INVALID
        transaction.is_successful = False
        transaction.save()
        return render(request, 'src/failure.html')


def check_transaction_pesapal(request, transaction_id):
    # get order status
    post_params = {
        'pesapal_merchant_reference': transaction_id,  # order_id
        'pesapal_transaction_tracking_id': transaction_id  # generated by pesapal
    }
    url = queryPaymentDetails(post_params)
    response = requests.get(url)
    print(response.json())


""" PesaPal Integration """
def pesapal_ipn():
    return 'IPN recieved'


""" Jenga API integration """
def payment_successful(request, project_id):
    project = Project.objects.filter(pk=project_id)
    if project:
        Transaction.objects.create(
            transaction_id=request.JSON.get('transactionId'),
            project=project,
            transaction_date=request.JSON.get('date'),
            amount=request.JSON.get('amount'),
            extra_data=request.JSON.get('extraData'),
            payment_mode=request.JSON.get('desc'),
            is_successful=True if request.JSON.get('status') == 'paid' else False
        )
        context = {
            'key_text': project.name,
            'project': project,
            'is_successful': True if request.JSON.get('status') == 'paid' else False
        }
        return render(request, 'src/success.html', context)
    else:
        messages.error(request, "Could not find the project!")
        context = {
            'key_text': "Error",
            'is_successful': False
        }
        return render(request, 'src/failure.html', context)


""" Jenga API integration """
def generate_token():
    url = "https://api-test.equitybankgroup.com/v1/token"

    payload = f"grant_type=password&merchantCode={settings.JENGA_USERNAME}&password={settings.JENGA_PASSWORD}"
    headers = {
        'authorization': settings.JENGA_API_KEY,
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.json())

    return response.json()['payment-token'] if response.status_code == 200 else ''


# Paypal Integration
@csrf_exempt
def paypal_checkout_success(request):
    if request.is_ajax():
        payment_data = json.loads(request.POST.get('response'))
        payment_reference = request.POST.get('type')
        ref_id = request.POST.get('ref_id', '')
        cart = request.POST.get('cart', '')
        amount = request.POST.get('amount')
        PhoneNumber = request.POST.get('phone', '')
        Address = request.POST.get('address', '')

        if int(payment_reference) == 1:
            add_online_learning_transaction(payment_data, amount, ref_id)
        elif int(payment_reference) == 2:
            add_ec_site_transaction(payment_data, amount, cart, PhoneNumber, Address)
        else:
            donation_transaction(payment_data, amount, ref_id)
        return JsonResponse({'message': 'Thank you'})

def add_online_learning_transaction(payment_data, amount, ref_id):
    booking = ProjectBookings.objects.filter(pk=ref_id).first()
    if booking:
        booking.is_paid = True
        booking.save()

        Transaction.objects.create(
            transaction_id=payment_data['id'],
            project=booking.project,
            booking=booking,
            transaction_date=datetime.now(),
            amount=Decimal(amount),
            full_name=f"{payment_data['payer']['name']['given_name']} {payment_data['payer']['name']['surname']}",
            extra_data="PayPal Payment",
            payment_mode="PayPal",
            is_successful=True
        )
        return True

def add_ec_site_transaction(payment_data, amount, cart, phone_number, address):
    order_items = json.loads(cart)

    order_id = uuid.uuid4()
    ref_id = str(order_id)[:8]
    new_order = Order.objects.create(
        public_id=order_id,
        ref_id=ref_id,
        buyer_name=f"{payment_data['payer']['name']['given_name']} {payment_data['payer']['name']['surname']}",
        buyer_email=f"{payment_data['payer']['email_address']}",
        buyer_address=address,
        buyer_phone_address=phone_number,
        amount=amount,
        is_paid=True,
        transaction_id=payment_data['id']
    )
    for item in order_items:
        item_ = Item.objects.get(pk=item['itemId'])
        OrderItems.objects.create(
            public_id=uuid.uuid4(),
            order=new_order,
            quantity=item['count'],
            price=item['price'],
            item=item_
        )
    return True

def donation_transaction(payment_data, amount, ref_id):
    transaction = DonationTransaction.objects.get(pk=ref_id)
    if transaction:
        transaction.transaction_id = payment_data['id']
        transaction.is_successful = True
        transaction.save()
        
        donation = Donation.objects.get(pk=transaction.donation.pk)
        donation.amount += int(amount)
        donation.save()

    return True
