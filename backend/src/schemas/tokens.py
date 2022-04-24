from datetime import datetime

from pydantic import BaseModel


class AuthTokensOut(BaseModel):
    expires_in: datetime
    token_type: str = "Bearer"
    access_token: str
    refresh_token: str
