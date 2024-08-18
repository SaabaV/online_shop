from celery import shared_task
from django.utils import timezone
from .models import Order


@shared_task
def delete_unpaid_orders():
    try:
        expiration_time = timezone.now() - timezone.timedelta(minutes=15)
        orders_to_delete = Order.objects.filter(status='pending', created_at__lt=expiration_time)
        print(f"Будут удалены заказы: {orders_to_delete}")
        orders_to_delete.delete()
    except Exception as e:
        print(f"Ошибка в delete_unpaid_orders: {str(e)}")
        raise
