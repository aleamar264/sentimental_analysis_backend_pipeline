from abc import ABC, abstractmethod
from typing import Any

import transformers
from schemas.analysis_schema import AnalysisFinancialModel, AnalysisModel
from transformers import pipeline

transformers.utils.logging.disable_default_handler()
transformers.utils.logging.disable_progress_bar()
transformers.utils.logging.disable_propagation()


class SentimentAnalysis(ABC):
    @abstractmethod
    def get_sentiment(
        self, answer_model: AnalysisModel | AnalysisFinancialModel
    ) -> list[dict[str, str]]:
        pass


class FinancialSentimentAnalysis(SentimentAnalysis):
    def get_sentiment(
        self, answer_model: AnalysisFinancialModel
    ) -> list[dict[str, Any]]:
        """
        The function `get_sentiment` uses a pre-trained transformer model to analyze the sentiment of input
        phrases and returns a list of dictionaries containing the sentiment labels and corresponding IDs.

        Args:
            answer_model (AnalysisFinancialModel): The `answer_model` parameter in the `get_sentiment` method is an
        instance of the `AnalysisFinancialModel` class. It contains the following attributes:

        Returns:
            The `get_sentiment` function returns a list of dictionaries, where each dictionary contains the
        sentiment label for a phrase in the `answer_model` along with the corresponding ID from the
        `answer_model`.
        """
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(answer_model.model.value)
        model = AutoModelForSequenceClassification.from_pretrained(
            answer_model.model.value
        )
        sentiment_pipeline = pipeline(
            "text-classification", model=model, tokenizer=tokenizer
        )
        sentiment = sentiment_pipeline(answer_model.phrase)
        response = [
            {phrase: feeling["label"], "id": answer_model.id}
            for phrase, feeling in zip(answer_model.phrase, sentiment)
        ]
        return response


class GeneralSentimentAnalysis(SentimentAnalysis):
    def get_sentiment(self, answer_model: AnalysisModel) -> list[dict[str, Any]]:
        """
        The function `get_sentiment` uses a sentiment analysis model to analyze phrases and returns a list
        of dictionaries containing the sentiment labels and corresponding IDs.

        Args:
            answer_model (AnalysisModel): The `answer_model` parameter in the `get_sentiment` method is an
        instance of the `AnalysisModel` class. It contains the following attributes:

        Returns:
            A list of dictionaries containing the sentiment label for each phrase in the input answer model,
        along with the corresponding ID from the answer model.
        """
        sentiment_pipeline = pipeline(model=answer_model.model.value)
        sentiment = sentiment_pipeline(answer_model.phrase)
        response = [
            {phrase: feeling["label"], "id": answer_model.id}
            for phrase, feeling in zip(answer_model.phrase, sentiment)
        ]
        return response
        return response
