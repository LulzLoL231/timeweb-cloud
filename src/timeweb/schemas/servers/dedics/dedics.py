# -*- coding: utf-8 -*-
'''Модели для работы с выделенными серверами'''
import json
from typing import Any
from enum import Enum
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field

from ...time_utils import Period
from ...base import ResponseWithMeta, BaseResponse


class ServerStatus(str, Enum):
    '''Статусы выделенных серверов'''
    INSTALLING = 'installing'
    INSTALED = 'installed'
    ON = 'on'
    OFF = 'off'


class DedicatedServer(BaseModel):
    '''Выделенный сервер'''
    id: int = Field(..., description='UID выделенного сервера.')
    cpu_description: str = Field(..., description='Описание CPU.')
    hdd_description: str = Field(..., description='Описание HDD.')
    ram_description: str = Field(..., description='Описание RAM.')
    created_at: datetime = Field(..., description='Дата создания.')
    ip: IPv4Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPv4.'
    )
    ipmi_ip: IPv4Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPMI.'
    )
    ipmi_login: str | None = Field(
        None, description='Логин для доступа к IPMI-консоли.'
    )
    ipmi_password: str | None = Field(
        None, description='Пароль для доступа к IPMI-консоли.'
    )
    ipv6: IPv6Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPv6.'
    )
    mode_id: int | None = Field(
        None, description='Внутренний дополнительный идентификатор сервера.'
    )
    name: str = Field(..., description='Название выделенного сервера.')
    comment: str = Field(..., description='Комментарий.')
    vnc_pass: str | None = Field(
        None, description='Пароль для доступа к VNC-консоли.'
    )
    status: ServerStatus = Field(..., description='Статус выделенного сервера.')
    os_id: int | None = Field(
        None, description='UID операционной системы.'
    )
    cp_id: int | None = Field(
        None, description='UID панели управления.'
    )
    bandwidth_id: int | None = Field(
        None, description='UID интернет-канала, установленного на выделенный сервер.'
    )
    network_drive_id: list[int] | None = Field(
        None, description='UID сетевых дисков, подключенных к выделенному серверу.'
    )
    additional_ip_addr_id: list[int] | None = Field(
        None, description='UID дополнительных IP-адресов, подключенных к выделенному серверу.'
    )
    plan_id: int | None = Field(
        None, description='UID списка дополнительных услуг выделенного сервера.'
    )
    price: int = Field(..., description='Цена выделенного сервера.')
    location: str = Field(..., description='Локация выделенного сервера.')
    autoinstall_ready: int = Field(
        ..., description=('Количество готовых к автоматической выдаче серверов. '
                          'Если значение равно 0, сервер будет установлен через инженеров.')
    )


class PaymentPeriods(Enum):
    '''Периоды оплаты'''
    P1M = Period('P1M')
    P3M = Period('P3M')
    P6M = Period('P6M')
    P1Y = Period('P1Y')


class PaymentPeriodsEncoder(json.JSONEncoder):
    '''PaymentPeriods encoder for JSON serialization.'''

    def default(self, obj: Any) -> Any:
        if isinstance(obj, PaymentPeriods):
            return str(obj.value)
        return json.JSONEncoder.default(self, obj)


class DedicatedServers(ResponseWithMeta):
    '''Ответ со списком выделенных серверов'''
    dedicated_servers: list[DedicatedServer] = Field(
        ..., description='Список выделенных серверов.'
    )


class DedicatedServerResponse(BaseResponse):
    '''Ответ с выделенным сервером'''
    dedicated_server: DedicatedServer = Field(
        ..., description='Выделенный сервер.'
    )
