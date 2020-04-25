from django.shortcuts import render
from django.contrib import messages
from Cheka.settings import JENGA_USERNAME, JENGA_PASSWORD, JENGA_API_KEY
from .utility_functions import *
import requests


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
    token = generate_token()
    context = {
        'categories': categories,
        'project': project,
        'key_text': project.name,
        'summary': f'${project.price}',
        'checkout_amount': int(project.price * 100),
        'thumbnail': project.thumbnail,
        'payment_token': token,
        'show-checkout': True if token else False
    }
    
    return render(request, 'src/detail.html', context)

def project_checkout(request, project_id):
    messages.info(request, "Requesting payment module")


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

def generate_token():
    url = "https://api-test.equitybankgroup.com/v1/token"

    payload = f"grant_type=password&merchantCode={JENGA_USERNAME}&password={JENGA_PASSWORD}"
    headers = {
        'authorization': JENGA_API_KEY,
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.json())

    return response.json()['payment-token'] if response.status_code == 200 else ''
