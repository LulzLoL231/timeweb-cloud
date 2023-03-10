# -*- coding: utf-8 -*-
'''Модели для работы с API токенами'''
from uuid import UUID
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData


class APIKey(BaseData):
    '''Модель API токена.

    Attributes:
        id (UUID): Уникальный идентификатор токена.
        created_at (datetime): Дата и время создания токена.
        name (str): Имя токена.
        expires_at (datetime | None): Дата истечения срока действия токена.
    '''
    id: UUID = Field(..., description='Уникальный идентификатор токена.')
    created_at: datetime = Field(
        ..., description='Дата и время создания токена.'
    )
    name: str = Field(..., description='Имя токена.')
    expired_at: datetime | None = Field(
        None, description='Дата истечения срока действия токена.'
    )


class CreatedAPIKey(APIKey):
    '''Модель созданного API токена.

    Attributes:
        token (str): Созданный токен, будет показан только один раз, его необходимо сохранить.
    '''
    token: str = Field(
        ..., description='Созданный токен, будет показан только один раз, его необходимо сохранить.'
    )


class APIKeysResponse(ResponseWithMeta):
    '''Модель ответа API токенов.

    Attributes:
        api_keys (list[APIKey] | None): Массив токенов.
    '''
    api_keys: list[APIKey] | None = Field(None, description='Массив токенов.')


class APIKeyResponse(BaseResponse):
    '''Модель ответа API токена.

    Attributes:
        api_key (APIKey): Токен.
    '''
    api_key: APIKey = Field(..., description='Токен.')


class CreateAPIKeyResponse(BaseResponse):
    '''Модель ответа созданного API токена.

    Attributes:
        api_key (CreatedAPIKey): Токен.
    '''
    api_key: CreatedAPIKey = Field(..., description='Токен.')
