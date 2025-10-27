from pydantic import BaseModel


class ResendTokenRequest(BaseModel):
    company_id: int
