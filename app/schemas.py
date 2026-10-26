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


class ModuleParticleCreate(BaseModel):
    difficulty: int = Field(ge=1, le=3)

    sentence_before: str = Field(max_length=255)
    sentence_after: str = Field(max_length=255)

    correct_answer: str = Field(min_length=1, max_length=50)
    wrong_answers: list[str] = Field(min_length=1, max_length=5)

    explanation: str = Field(max_length=1000)
    

class ModuleParticlePublic(BaseModel): 
    id: int
    difficulty: int
    
    sentence_before: str
    sentence_after: str

    possible_answers: list[str] # I have to remember to merge correct_answer and wrong_answers first