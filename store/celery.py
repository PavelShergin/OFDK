import os

from celery import Celery

# Установка максимальной памяти для каждого дочернего процесса в килобайтах
worker_max_memory_per_child = 400000000  # Здесь можно указать желаемое значение в килобайтах

# Установка переменной окружения для задания Django settings module по умолчанию для программы 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

# Создание экземпляра Celery приложения
app = Celery('store')

# Установка параметров подключения к Redis
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Использование строки здесь означает, что рабочему процессу не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='CELERY' означает, что все ключи конфигурации, связанные с Celery,
#   должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка модулей задач из всех зарегистрированных Django приложений.
app.autodiscover_tasks()

# Установка максимальной памяти для каждого дочернего процесса в Celery
app.conf.worker_max_memory_per_child = worker_max_memory_per_child
