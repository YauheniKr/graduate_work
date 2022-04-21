from pydantic import BaseModel


class CheckoutInfo(BaseModel):
    checkout_url: str
    checkout_id: str
