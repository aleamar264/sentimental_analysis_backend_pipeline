from transformers import pipeline
from backend_pipeline.schemas.analysis_schema import AnalysisModel
from abc import ABC, abstractmethod


class SentimentAnalysis(ABC):
    @abstractmethod
    def get_sentiment(
        self, answer_model: AnalysisModel
    ) -> list[dict[str, str]]:
        pass


class FinancialSentimentAnalysis(SentimentAnalysis):
    def get_sentiment(
        self, answer_model: AnalysisModel
    ) -> list[dict[str, str]]:
        from transformers import (
            AutoTokenizer,
            AutoModelForSequenceClassification,
        )

        tokenizer = AutoTokenizer.from_pretrained(answer_model.model)
        model = AutoModelForSequenceClassification.from_pretrained(
            answer_model.model
        )
        sentiment_pipeline = pipeline(
            "text-classification", model=model, tokenizer=tokenizer
        )
        sentiment = sentiment_pipeline(answer_model.phrase)
        response = [
            {phrase: feeling["label"]}
            for phrase, feeling in zip(answer_model.phrase, sentiment)
        ]
        return response


class GeneralSentimentAnalysis(SentimentAnalysis):
    def get_sentiment(
        self, answer_model: AnalysisModel
    ) -> list[dict[str, str]]:
        sentiment_pipeline = pipeline(model=answer_model.model)
        sentiment = sentiment_pipeline(answer_model.phrase)
        response = [
            {phrase: feeling["label"]}
            for phrase, feeling in zip(answer_model.phrase, sentiment)
        ]
        return response
