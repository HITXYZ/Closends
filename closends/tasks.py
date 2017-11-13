import time
from celery.task import task
from celery.task import periodic_task
from celery.schedules import crontab
from django.contrib.auth.models import User

@task(name="send_email")
def sendmail(email):
    print('start send email to %s' % email)
    time.sleep(10)
    return True

@periodic_task(run_every=(crontab(minute='*/1')), name="spider")
def some_task():
    user = User.objects.all()[0]
    print(user.email)