# -*- coding: utf-8 -*-
from uuid import UUID

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    '''Базовая модель ответа'''
    response_id: UUID | None = Field(
        None, description=('В большинстве случае в ответе будет содержаться '
                           'уникальный идентификатор ответа в формате UUIDv4, '
                           'который однозначно указывает на ваш запрос внутри '
                           'нашей системы. Если вам потребуется задать вопрос '
                           'нашей поддержке, то приложив к вопросу этот '
                           'идентификатор, мы сможем найти ответ на него '
                           'намного быстрее.')
    )


class BaseMeta(BaseModel):
    '''Базовая модель мета-данных'''
    total: int | None = Field(
        None, description='Общее количество элементов в коллекции.'
    )


class ResponseWithMeta(BaseResponse):
    '''Модель ответа с мета-данными'''
    meta: BaseMeta | None = Field(None, description='Мета-данные.')
