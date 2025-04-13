import os

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

def generate_activation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    if os.getenv('ENVIRONMENT') == 'development':
        activation_link = f"http://127.0.0.1:8000/activate/{uid}/{token}/"
    else:
        activation_link = f"https://djangogramm1-1620dd96cc61.herokuapp.com/activate/{uid}/{token}"
    return activation_link


def send_activation_email(user, activation_link):
    subject = 'Account activation for Djangogram'
    message = f'Hi, {user.username}!\n\nFollow the link to activate your account:\n{activation_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
