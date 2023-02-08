# -*- coding: utf-8 -*-
'''Модели для работы с SSH ключами'''
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta, BaseResponse


class Server(BaseModel):
    '''Модель сервера'''
    id: UUID = Field(..., description='Уникальный идентификатор сервера.')
    name: str = Field(..., description='Название сервера.')


class SSHKey(BaseModel):
    '''Модель SSH ключа'''
    id: UUID = Field(..., description='Уникальный идентификатор SSH ключа.')
    name: str = Field(..., description='Название SSH ключа.')
    body: str = Field(..., description='Тело SSH-ключа.')
    created_at: datetime = Field(
        ..., description='Дата и время создания SSH ключа.'
    )
    used_by: list[Server] = Field(
        ..., description='Массив серверов, на которых используется SSH ключ.'
    )
    is_default: bool = Field(
        ..., description='Будет ли выбираться SSh-ключ по умолчанию при создании сервера'
    )


class SSHKeysArray(ResponseWithMeta):
    '''Модель ответа SSH ключей'''
    ssh_keys: list[SSHKey] = Field(..., description='Массив SSH ключей.')


class CreateSSHKeyResponse(BaseResponse):
    '''Модель ответа созданного SSH ключа'''
    ssh_key: SSHKey = Field(..., description='SSH ключ.')


class SSHKeyResponse(ResponseWithMeta):
    '''Модель ответа SSH ключа'''
    ssh_key: SSHKey = Field(..., description='SSH ключ.')
