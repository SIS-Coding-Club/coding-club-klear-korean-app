from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserLogin(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel): 
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)