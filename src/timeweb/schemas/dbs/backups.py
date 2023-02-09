# -*- coding: utf-8 -*-
'''Модели для работы с Бэкапами баз данных'''
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta, BaseResponse


class BackupStatus(str, Enum):
    '''Статусы бэкапов'''
    PRECREATE = 'precreate'
    DELETE = 'delete'
    SHUTDOWN = 'shutdown'
    RECOVER = 'recover'
    CREATE = 'create'
    FAIL = 'fail'
    DONE = 'done'


class BackupType(str, Enum):
    '''Типы бэкапов'''
    MANUAL = 'manual'
    AUTO = 'auto'


class Backup(BaseModel):
    '''Бэкап базы данных'''
    id: int = Field(..., description='ID бэкапа.')
    name: str = Field(..., description='Имя бэкапа.')
    comment: str | None = Field(
        None, description='Комментарий к бэкапу.'
    )
    created_at: datetime = Field(
        ..., description='Дата создания бэкапа.'
    )
    status: BackupStatus = Field(
        ..., description='Статус бэкапа.'
    )
    size: int = Field(..., description='Размер бэкапа (Мб).')
    type: BackupType = Field(..., description='Тип бэкапа.')


class BackupArray(ResponseWithMeta):
    '''Массив бэкапов'''
    backups: list[Backup] = Field(..., description='Массив бэкапов.')


class BackupResponse(BaseResponse):
    '''Бэкап'''
    backup: Backup = Field(..., description='Бэкап.')
