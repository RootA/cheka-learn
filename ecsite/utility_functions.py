from django.core.mail import send_mail
from .models import Category


class Mail:
    def __init__(self):
        self.full_name = self.full_name
        self.email = self.email
        self.subject = self.subject
        self.message = self.message

    def sendMail(self, *args):
        print("We are here", *args)
        list_to = [
            'amwathi@fluidtechglobal.com'
        ]
        send_mail(self.subject, self.message, self.email, list_to, fail_silently=False)


class Helpers:
    @staticmethod
    def fetchCategories():
        categories = Category.objects.filter(is_active=True)
        return categories
