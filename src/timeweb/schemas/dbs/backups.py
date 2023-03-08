# -*- coding: utf-8 -*-
'''Модели для работы с Бэкапами баз данных'''
from enum import Enum
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData


class BackupStatus(str, Enum):
    '''Статусы бэкапов

    Attributes:
        PRECREATE (str): precreate
        DELETE (str): delete
        SHUTDOWN (str): shutdown
        RECOVER (str): recover
        CREATE (str): create
        FAIL (str): fail
        DONE (str): done
    '''
    PRECREATE = 'precreate'
    DELETE = 'delete'
    SHUTDOWN = 'shutdown'
    RECOVER = 'recover'
    CREATE = 'create'
    FAIL = 'fail'
    DONE = 'done'


class BackupType(str, Enum):
    '''Типы бэкапов

    Attributes:
        MANUAL (str): manual
        AUTO (str): auto
    '''
    MANUAL = 'manual'
    AUTO = 'auto'


class Backup(BaseData):
    '''Бэкап базы данных

    Attributes:
        id (int): ID бэкапа.
        name (str): Имя бэкапа.
        comment (str | None): Комментарий к бэкапу.
        created_at (datetime): Дата создания бэкапа.
        status (BackupStatus): Статус бэкапа.
        size (int): Размер бэкапа (Мб).
        type (BackupType): Тип бэкапа.
    '''
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
    '''Массив бэкапов

    Attributes:
        backups (list[Backup]): Массив бэкапов.
    '''
    backups: list[Backup] = Field(..., description='Массив бэкапов.')


class BackupResponse(BaseResponse):
    '''Бэкап

    Attributes:
        backup (Backup): Бэкап
    '''
    backup: Backup = Field(..., description='Бэкап.')
