from celery import shared_task
from api import sentiment_analysis


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="Sentimental_Analisys:get_sentiment_task",
)
def get_sentiment_task(self): ...
