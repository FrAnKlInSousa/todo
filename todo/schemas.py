from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from todo.models import TodoState


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3)
    description: str | None = Field(default=None, min_length=3)
    state: TodoState | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState = Field(default=TodoState.todo)


class TodoPublic(TodoSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class Sexo(str, Enum):
    MULHER = 'mulher'
    HOMEM = 'homem'

    @property
    def sexo(self) -> float:
        return {Sexo.HOMEM: 5, Sexo.MULHER: -161}[self]


class NivelAtividadeFisica(str, Enum):
    SEDENTARIO = 'sedentario'
    LEVE = 'leve'
    MODERADO = 'moderado'
    INTENSO = 'intenso'
    ATLETA = 'atleta'

    @property
    def fator(self) -> float:
        fatores = {
            NivelAtividadeFisica.SEDENTARIO: 1.2,
            NivelAtividadeFisica.LEVE: 1.375,
            NivelAtividadeFisica.MODERADO: 1.5,
            NivelAtividadeFisica.INTENSO: 1.725,
            NivelAtividadeFisica.ATLETA: 1.9,
        }

        return fatores[self]


class Nutri(BaseModel):
    peso: float = Field(ge=10, le=500)
    altura: int = Field(ge=30, le=300)
    idade: int = Field(ge=1, le=150)
    sexo: Sexo = Field(
        examples=[Sexo.MULHER, Sexo.HOMEM], description='sexo do paciente'
    )
    nivel_atividade_fisica: NivelAtividadeFisica
