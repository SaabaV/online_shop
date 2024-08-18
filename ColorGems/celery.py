from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ColorGems.settings')

app = Celery('ColorGems')

# Загружаем настройки из файла settings.py по ключу CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()

# Пример расписания для автоматического удаления неоплаченных заказов
app.conf.beat_schedule = {
    'delete-unpaid-orders-every-15-minutes': {
        'task': 'user_cart.tasks.delete_unpaid_orders',
        'schedule': crontab(minute='*/15'),
    },
}

