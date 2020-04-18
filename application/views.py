from django.shortcuts import render
from .utility_functions import *

def index(request):
    categories = fetch_categories()
    projects = fetch_projects()

    context = {
        'categories': categories,
        'projects': projects
    }
    return render(request, '', context)


def project_detail(request, project_id):
    categories = fetch_categories()
    project = fetch_single_project(project_id)

    context = {
        'categories': categories,
        'projects': project
    }
    return render(request, '', context)