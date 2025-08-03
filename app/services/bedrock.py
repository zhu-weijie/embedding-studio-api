import json
from typing import List

import boto3

from app.core.config import settings


class BedrockService:
    def __init__(self):

        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.model_id = "amazon.titan-embed-text-v2:0"

    def generate_embedding(
        self, text: str, dimensions: int = 1024, normalize: bool = True
    ) -> List[float]:
        body = json.dumps(
            {
                "inputText": text,
                "dimensions": dimensions,
                "normalize": normalize,
            }
        )

        response = self.client.invoke_model(
            body=body,
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")


bedrock_service = BedrockService()
