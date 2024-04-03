from fastapi import APIRouter
from celery import group
from fastapi.responses import JSONResponse

from api import sentiment_analysis
from celery_tasks.tasks import get_sentiment_task, get_financial_sentiment
from config.celery_utils import get_task_info
from schemas.analysis_schema import AnalysisModel


router = APIRouter(
    prefix="/analysis",
    tags=["Sentiment Analysis"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def get_analysis(question: AnalysisModel) -> dict:
    data: dict = {}
    return data


@router.post("/async")
async def get_analysis_async(question: AnalysisModel) -> JSONResponse:
    task = get_sentiment_task.apply_async(args=[question.phrase])
    return JSONResponse({"task_id": task.id})


@router.post("/async/financial")
async def get_finanacial_sentiment_async(
    question: AnalysisModel,
) -> JSONResponse:
    task = get_financial_sentiment.apply_async(args=[question.phrase])
    return JSONResponse({"task_id": task.id})


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """Return the status of the submited task

    Args:
        task_id (str): Id of the task
    """

    return get_task_info(task_id)


@router.post("/parallel")
async def get_analysis_parallel(question: AnalysisModel) -> dict:
    data: dict = {}
    tasks = []
    # here come the task
    job = group(tasks)
    result = job.apply_async()
    ret_values = result.get(disable_sync_subtasks=False)
    for result in ret_values:
        data.update(result)
    return data
