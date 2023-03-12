# -*- coding: utf-8 -*-
'''Модели для работы с SSH ключами'''
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData


class Server(BaseData):
    '''Модель сервера.

    Attributes:
        id (int): Уникальный идентификатор сервера.
        name (str): Название сервера.
    '''
    id: int = Field(..., description='Уникальный идентификатор сервера.')
    name: str = Field(..., description='Название сервера.')


class SSHKey(BaseData):
    '''Модель SSH ключа.

    Attributes:
        id (int): Уникальный идентификатор SSH ключа.
        name (str): Название SSH ключа.
        body (str): Тело SSH-ключа.
        created_at (datetime): Дата и время создания SSH ключа.
        used_by (list[Server]): Массив серверов, на которых используется SSH ключ.
        is_default (bool): Будет ли выбираться SSH-ключ по умолчанию при создании сервера
    '''
    id: int = Field(..., description='Уникальный идентификатор SSH ключа.')
    name: str = Field(..., description='Название SSH ключа.')
    body: str = Field(..., description='Тело SSH-ключа.')
    created_at: datetime = Field(
        ..., description='Дата и время создания SSH ключа.'
    )
    used_by: list[Server] = Field(
        ..., description='Массив серверов, на которых используется SSH ключ.'
    )
    is_default: bool = Field(
        ..., description='Будет ли выбираться SSH-ключ по умолчанию при создании сервера'
    )


class SSHKeysArray(ResponseWithMeta):
    '''Модель ответа SSH ключей.

    Attributes:
        ssh_keys (list[SSHKey]): Массив SSH ключей.
    '''
    ssh_keys: list[SSHKey] = Field(..., description='Массив SSH ключей.')


class CreateSSHKeyResponse(BaseResponse):
    '''Модель ответа созданного SSH ключа.

    Attributes:
        ssh_key (SSHKey): SSH ключ.
    '''
    ssh_key: SSHKey = Field(..., description='SSH ключ.')


class SSHKeyResponse(ResponseWithMeta):
    '''Модель ответа SSH ключа.

    Attributes:
        ssh_key (SSHKey): SSH ключ.
    '''
    ssh_key: SSHKey = Field(..., description='SSH ключ.')
