from pydantic import BaseModel


class ChatInitMessage(BaseModel):
    session_id: str | None = None
    prompt: str
