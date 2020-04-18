from .models import *

def fetch_categories():
    return Category.objects.all()

def fetch_projects():
    return Project.objects.filter(is_active=True)

def fetch_single_project(project_id):
    return Project.objects.get(pk=project_id)

def fetch_transactions():
    return Project.objects.all()
