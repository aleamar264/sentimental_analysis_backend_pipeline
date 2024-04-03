from api import sentiment_analysis
from celery import shared_task
from schemas.analysis_schema import AnalysisModel


@shared_task(
	bind=True,
	autoretry_for=(Exception,),
	retry_backoff=True,
	retry_kwargs={"max_retries": 5},
	name="Sentimental_Analisys:get_sentiment_task",
)
def get_sentiment_task(self, question: AnalysisModel):
	analysis = sentiment_analysis.GeneralSentimentAnalysis()
	result = analysis.get_sentiment(question)
	return result


@shared_task(
	bind=True,
	autoretry_for=(Exception,),
	retry_backoff=True,
	retry_kwargs={"max_retries": 5},
	name="Sentimental_Analisys:get_financial_sentiment_task",
)
def get_financial_sentiment_task(self, question: AnalysisModel):
	analysis = sentiment_analysis.FinancialSentimentAnalysis()
	result = analysis.get_sentiment(question)
	return result
