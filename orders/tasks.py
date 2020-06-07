from celery import task
from django.core.mail import send_mail
from .models import Order

@task 
def order_created(order_id):
    """
    task to send an email notification when an order
    is successfully created 
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n You have successfuly placed an order'\
              f'Your order ID is {order.id}'
    mail_sent = send_mail(subject,message,'admin@onlineshop.com',[order.email])

    return mail_sent
    """
    always recommended to only pass ids to task functions 
    """