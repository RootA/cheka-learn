from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, FormView, CreateView

from .utility_functions import *
from .forms import CommentForm

import requests

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
        'key_text': 'Cheka',
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
    # token = generate_token()
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
    }

    # token = generate_token()
    # context = {
    #     'categories': categories,
    #     'projects': project
    #     'project': project,
    #     'key_text': project.name,
    #     'summary': f'${project.price}',
    #     'checkout_amount': int(project.price * 100),
    #     'thumbnail': project.thumbnail,
    #     'payment_token': token,
    #     'show-checkout': True if token else False
    # }
    return render(request, 'src/detail.html', context)


def project_checkout(request, project_id):
    project = fetch_single_project(project_id)
    request_data = {
        'Amount': str(int(project.price)),
        'Currency': 'USD',
        'Description': project.name,
        'Type': 'MERCHANT',
        'Reference': project.ref_id,
        'FirstName': request.POST.get('first_name'),
        'LastName': request.POST.get('last_name'),
        'Email': request.POST.get('email'),
    }
    post_params = {
        'oauth_callback': f'http://localhost:8000/project/payment'
    }
    # build url to redirect user to confirm payment
    url = postDirectOrder(post_params, request_data)
    context = {
        'url': url,
        'title': 'Checkout'
    }
    return render(request, 'src/checkout.html', context)


class DonationsView(ListView):
    model = Donation
    template_name = 'src/donations.html'
    context_object_name = 'donations'


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
