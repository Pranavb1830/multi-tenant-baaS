from pydantic import BaseModel, ConfigDict, Field # pyright: ignore[reportMissingImports]

class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8, max_length=60)

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str = Field(..., min_length=8, max_length=60)

class ProjectCreate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    api_key: str

    model_config = ConfigDict(from_attributes=True)