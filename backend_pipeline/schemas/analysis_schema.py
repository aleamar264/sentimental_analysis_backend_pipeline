from pydantic import BaseModel


class AnalysisModel(BaseModel):
	id: int | None = None
	phrase: list[str]
	model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"

	model_config = {
		"json_schema_extra": {
			"examples": [
				{
					"id": None,
					"phrase": ["I love this movie!"],
					"model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
				}
			]
		}
	}
