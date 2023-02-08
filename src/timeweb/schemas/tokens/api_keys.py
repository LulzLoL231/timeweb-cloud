# -*- coding: utf-8 -*-
'''Модели для работы с API токенами'''
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta, BaseResponse


class APIKey(BaseModel):
    '''Модель API токена'''
    id: UUID = Field(..., description='Уникальный идентификатор токена.')
    created_at: datetime = Field(
        ..., description='Дата и время создания токена.'
    )
    name: str = Field(..., description='Имя  токена.')
    expires_at: datetime | None = Field(
        None, description='Дата истечения срока действия токена.'
    )


class CreatedAPIKey(APIKey):
    '''Модель созданного API токена'''
    token: str = Field(
        ..., description='Созданный токен, будет показан только один раз, его необходимо сохранить.'
    )


class APIKeysResponse(ResponseWithMeta):
    '''Модель ответа API токенов'''
    api_keys: list[APIKey] | None = Field(None, description='Массив токенов.')


class APIKeyResponse(BaseResponse):
    '''Модель ответа API токена'''
    api_key: APIKey = Field(..., description='Токен.')


class CreateAPIKeyResponse(BaseResponse):
    '''Модель ответа созданного API токена'''
    api_key: CreatedAPIKey = Field(..., description='Токен.')
