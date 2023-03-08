# -*- coding: utf-8 -*-
'''Модели для работы с S3 трансфером'''
from enum import Enum

from pydantic import Field

from ..base import ResponseWithMeta, BaseData


class TransferStatus(str, Enum):
    '''Статус трансфера'''
    STARTED = 'started'
    SUSPENDED = 'suspended'
    FAILED = 'failed'


class TransferError(BaseData):
    '''Модель ошибки трансфера

    Attributes:
        value (str): Текст ошибки
        try_count (int): Количество попыток.

    Note:
        Поле `try` зарезервировано в Python, поэтому используется `try_count`.
        Для получения значения `try`, используйте `obj.json(by_alias=True)` или
        `obj.dict(by_alias=True)`.'''
    value: str = Field(..., description='Текст ошибки')
    try_count: int = Field(..., description='Количество попыток.', alias='try')


class Transfer(BaseData):
    '''Модель трансфера.

    Attributes:
        status (TransferStatus): Статус трансфера
        tries (int): Количество попыток
        total_count (int): Общее количество затронутых объектов.
        total_size (int): Общий размер затронутых объектов.
        uploaded_count (int): Количество перемещенных объектов.
        uploaded_size (int): Размер перемещенных объектов.
        errors (list[TransferError] | None): Описание ошибки трансфера
    '''
    status: TransferStatus = Field(..., description='Статус трансфера')
    tries: int = Field(..., description='Количество попыток')
    total_count: int = Field(
        ..., description='Общее количество затронутых объектов.'
    )
    total_size: int = Field(
        ..., description='Общий размер затронутых объектов.'
    )
    uploaded_count: int = Field(
        ..., description='Количество перемещенных объектов.'
    )
    uploaded_size: int = Field(
        ..., description='Размер перемещенных объектов.'
    )
    errors: list[TransferError] | None = Field(
        None, description='Описание ошибки трансфера'
    )


class TransferResponse(ResponseWithMeta):
    '''Модель ответа трансфера.

    Attributes:
        transfer_status (Transfer): Трансфер
    '''
    transfer_status: Transfer
