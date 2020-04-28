from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<project_id>', views.project_detail, name='project-detail'),
    # path('project/<project_id>/process', views.project_checkout, name='project-detail'),
    path('project/<ref_id>/success', views.payment_successful, name='payment-successful'),
    path('payment/<project_id>', TemplateView.as_view(template_name="src/detail.html"), name='payment'),
]
