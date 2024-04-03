from functools import wraps

from api import sentiment_analysis
from celery_tools.celery_tasks.tasks import (
	get_financial_sentiment_task,
	get_sentiment_task,
)
from celery_tools.config.celery_utils import get_task_info
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from icecream import icecream
from redis import Redis
from schemas.analysis_schema import AnalysisModel
from utils.fastapi.auth.dependencies import user_dependency

r = Redis(host="cache", port=6379)

router = APIRouter(
	prefix="/analysis",
	tags=["Sentiment Analysis"],
	responses={404: {"description": "Not found"}},
)


def cache_utils(func):
	@wraps(func)
	def wrapper(question, user):
		response = [
			{
				phrase.strip(): r.hget(
					name=f"user_id->{user.get("id")}", key=phrase.strip()
				).decode()
			}
			for phrase in question.phrase
			if r.hexists(key=phrase.strip(), name=f"user_id->{user.get("id")}")
		]
		# icecream.ic(response)
		icecream.ic(
			r.hget(key=question.phrase[0].strip(), name=f"user_id->{user.get("id")}")
		)
		icecream.ic(
			r.hexists(key=question.phrase[0].strip(), name=f"user_id->{user.get("id")}")
		)
		if response:
			icecream.ic("I have cache")
			return JSONResponse(content=response, status_code=200)
		return func(question, user)

	return wrapper


@router.post("/")
@cache_utils
async def get_analysis(question: AnalysisModel, user: user_dependency) -> JSONResponse:
	"""
	This are the models that work
	```python
	"general_models": [
	    "siebert/sentiment-roberta-large-english",
	    "cardiffnlp/twitter-roberta-base-sentiment-latest",
	    ],
	```

	Args:
	    question (AnalysisModel):
	Return:
	    JSONResponse: Response with the sentiment analysis of the question.
	"""
	question.id = user.get("id")
	response = sentiment_analysis.GeneralSentimentAnalysis().get_sentiment(question)
	for res, phrase in zip(response, question.phrase):
		r.hset(name=f"user_id->{user.get("id")}", mapping=res)
	return JSONResponse(content=response, status_code=200)


@router.post("/financial")
@cache_utils
def get_analysis_financial(
	question: AnalysisModel, user: user_dependency
) -> JSONResponse:
	"""
	```python
	"financial_models": [
	                "Jean-Baptiste/roberta-large-financial-news-sentiment-en",
	                "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
	            ],
	```
	Args:
	    question (AnalysisModel):
	Return:
	    JSONResponse: Response with the sentiment analysis of the questi
	"""
	question.id = user.get("id")
	response = sentiment_analysis.FinancialSentimentAnalysis().get_sentiment(question)
	for res, phrase in zip(response, question.phrase):
		r.hset(name=f"user_id->{user.get("id")}", mapping=res)
	return JSONResponse(content=response, status_code=200)


@router.post("/async")
async def get_analysis_async(
	question: AnalysisModel, user: user_dependency
) -> JSONResponse:
	"""
	This have the same behavior like the endpoint analysis/, but the difference is that this is asyncronous and use rabbitmq and celery.
	"""
	question.id = user.get("id")
	task = get_sentiment_task.apply_async(args=[question])
	return JSONResponse({"task_id": task.id})


@router.post("/async/financial")
async def get_finanacial_sentiment_async(
	question: AnalysisModel,
	user: user_dependency,
) -> JSONResponse:
	"""
	This have the same behavior like the endpoint analysis/financial, but the difference is that this is asyncronous and use rabbitmq and celery.
	"""
	question.id = user.get("id")
	task = get_financial_sentiment_task.apply_async(args=[question])
	return JSONResponse({"task_id": task.id})


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
	"""Return the status of the submited task

	Args:
	    task_id (str): Id of the task
	"""

	return get_task_info(task_id)
	return get_task_info(task_id)
	return get_task_info(task_id)
	return get_task_info(task_id)
