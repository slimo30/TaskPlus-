from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskPlus.settings')

app = Celery('TaskPlus')  # Replace 'TaskPlus' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
@app.task
def long_running_task(name):
    # Perform some time-consuming task here
    print(f"Task completed for {name}")
    return f"Task completed for {name}"
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)