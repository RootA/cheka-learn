from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from .utility_functions import *
import requests
import pesapal
from .payment import postDirectOrder, queryPaymentStatus


def index(request):
    categories = fetch_categories()
    projects = fetch_projects()

    context = {
        'categories': categories,
        'projects': projects,
        'hero_text': 'Build Your English language Skills With',
        'key_text': 'Cheka TV',
        'summary': 'We offer you one to one lessons with the Cheka TV staff',
        'thumbnail': '/img/hero-img.png'
    }
    return render(request, 'src/index.html', context)


def project_detail(request, project_id):
    categories = fetch_categories()
    project = fetch_single_project(project_id)
    request_data = {
        'Amount': str(int(project.price)),
        'Description': project.name,
        'Type': 'MERCHANT',
        'Reference': project.ref_id,
        'PhoneNumber': '0731966124'
    }
    post_params = {
        'oauth_callback': f'https://localhost:8000/project/{project.ref_id}/success'
    }
    # build url to redirect user to confirm payment
    url = postDirectOrder(post_params, request_data)
    context = {
        'categories': categories,
        'project': project,
        'key_text': project.name,
        'summary': f'${project.price}',
        'checkout_amount': int(project.price * 100),
        'thumbnail': project.thumbnail,
        'url': url
    }

    response = render(request, 'src/detail.html', context)
    return response


pesapal.consumer_key = settings.PESAPAL_CONSUMER_KEY
pesapal.consumer_secret = settings.PESAPAL_SECRET_KEY
pesapal.testing = settings.TESTING


def project_checkout(request, project_id):
    project = fetch_single_project(project_id)
    request_data = {
        'Amount': str(int(project.price)),
        'Description': project.name,
        'Type': 'MERCHANT',
        'Reference': project.ref_id,
        'PhoneNumber': '0731966124'
    }
    post_params = {
        'oauth_callback': f'https://localhost:8000/project/{project.ref_id}/success'
    }
    # build url to redirect user to confirm payment
    url = postDirectOrder(post_params, request_data)
    response = HttpResponseRedirect(url)
    return response


def pesapal_callback(request, ref_id):
    print(request)
    return 'Success'


def check_transaction_pesapal():
    # get order status
    post_params = {
        'pesapal_merchant_reference': '000',
        'pesapal_transaction_tracking_id': '000'
    }
    url = queryPaymentStatus(post_params)
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
