from celery import shared_task


@shared_task
def celery_test_work(a, b):
    print("Celery Работаетa !!!")
    c = a + b
    print("Результат: ", c)