from io import BytesIO
from celery import task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@task
def payment_completed(order_id):
    """
    Task to send an email notification when an oreder 
    is successfully created
    """

    order = Order.objects.get(id=order_id)
    #create invoice e-mail
    subject = f'<y shop - EE Invoice no. {order.id}'
    message =  'please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@onlineshop.com',[order.email])

    #send e-mail
    email.send()