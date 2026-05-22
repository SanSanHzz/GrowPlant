from pydantic import BaseModel


class WebhookResponse(BaseModel):
    status: str
    delivery_id: str
