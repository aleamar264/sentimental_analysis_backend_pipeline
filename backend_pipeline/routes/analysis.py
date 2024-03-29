from fastapi import APIRouter
from celery import group
from fastapi.responses import JSONResponse

from api import sentiment_analysis
from celery_tasks.tasks import get_sentiment_task
from config.celery_utils import get_task_info
from schemas.analysis_schema import AnalysisModel
from 

router = APIRouter(
    prefix="/analysis",
    tags=["Sentiment Analysis"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def get_analysis()