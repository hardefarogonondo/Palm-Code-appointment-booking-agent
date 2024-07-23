from pydantic import BaseModel


class Message(BaseModel):
    content: str
    id: str


class OuterMessage(BaseModel):
    message: Message
