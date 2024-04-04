from enum import Enum


from pydantic import BaseModel


class GeneralModel(str, Enum):
    large_english = "siebert/sentiment-roberta-large-english"
    twitter = "cardiffnlp/twitter-roberta-base-sentiment-latest"


class FinancialModel(str, Enum):
    financial_canada_news = "Jean-Baptiste/roberta-large-financial-news-sentiment-en"
    financial_news = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"


class AnalysisModel(BaseModel):
    id: int | None = None
    phrase: list[str]
    model: GeneralModel = GeneralModel.large_english

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": None,
                    "phrase": ["I love this movie!"],
                    "model": GeneralModel.large_english,
                }
            ]
        }
    }


class AnalysisFinancialModel(BaseModel):
    id: int | None = None
    phrase: list[str]
    model: FinancialModel = FinancialModel.financial_news

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": None,
                    "phrase": ["I love this movie!"],
                    "model": FinancialModel.financial_news,
                }
            ]
        }
    }
