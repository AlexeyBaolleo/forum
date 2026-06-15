from pydantic import BaseModel, Field

from uuid import UUID

class BoardBase(BaseModel):
    title: str = Field(max_length=150, min_length=1)
    description: str = Field(max_length=600)


class BoardCreate(BoardBase):
    pass


class BoardView(BoardBase):
    uuid: UUID
    creator_uuid: UUID