# -*- coding: utf-8 -*-
from enum import Enum
from ipaddress import IPv4Address

from pydantic import Field, BaseModel

from ..base import BaseResponse


class RestrictionsStatus(BaseModel):
    is_enabled: bool = Field(..., description='Включены ли ограничения.')


class AddIPStatus(str, Enum):
    '''Статус добавления IP адреса.

    Attributes:
        SUCCESS (str): IP адрес успешно добавлен.
        CONFLICT (str): IP адрес уже существует.
    '''
    SUCCESS = 'success'
    CONFLICT = 'conflict'


class AddedIP(BaseModel):
    '''Статус добавленного IP адреса.

    Attributes:
        value (IPv4Address): IP адрес.
        status (AddIPStatus): Статус добавления IP адреса.
    '''
    value: IPv4Address = Field(..., description='IP адрес.')
    status: AddIPStatus = Field(..., description='Статус добавления IP адреса.')


class AddIP(BaseResponse):
    '''Список добавленных IP адресов.

    Attributes:
        ips (list[AddedIP]): Статус добавленного IP адреса.
    '''
    ips: list[AddedIP] = Field(..., description='Статус добавленного IP адреса.')


class RemoveIPStatus(str, Enum):
    '''Статус удаления IP адреса.

    Attributes:
        SUCCESS (str): IP адрес успешно удален.
        NOT_FOUND (str): IP адрес не найден.
    '''
    SUCCESS = 'success'
    NOT_FOUND = 'not_found'


class RemovedIP(BaseModel):
    '''Статус удаленного IP адреса.

    Attributes:
        value (IPv4Address): IP адрес.
        status (RemoveIPStatus): Статус удаления IP адреса.
    '''
    value: IPv4Address = Field(..., description='IP адрес.')
    status: RemoveIPStatus = Field(..., description='Статус удаления IP адреса.')


class RemoveIP(BaseResponse):
    '''Список удаленных IP адресов.

    Attributes:
        ips (list[RemovedIP]): Статус удаленного IP адреса.
    '''
    ips: list[RemovedIP] = Field(..., description='Статус удаленного IP адреса.')
