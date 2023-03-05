# -*- coding: utf-8 -*-
'''Модели для работы с облачными серверами'''
from enum import Enum
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import Field

from ...base import ResponseWithMeta, BaseResponse, BaseData


class OSNames(str, Enum):
    '''Имена ОС'''
    Bitrix = 'bitrix'
    BrainyCP = 'brainycp'
    CentOS = 'centos'
    Debian = 'debian'
    Fedora = 'fedora'
    FreeBSD = 'freebsd'
    Gentoo = 'gentoo'
    RouterOS = 'routeros'
    Ubuntu = 'ubuntu'
    Windows = 'windows'


class VDSOS(BaseData):
    '''Модель ОС сервера'''
    id: int = Field(..., description='UID ОС')
    name: OSNames = Field(..., description='Тип ОС')
    version: str | None = Field(None, description='Версия ОС')


class Software(BaseData):
    '''ПО из маркетплейса'''
    id: int = Field(..., description='UID ПО')
    name: str = Field(..., description='Название ПО')


class BootMode(str, Enum):
    '''Режим загрузки ОС'''
    STANDART = 'std'
    SINGLE = 'single'
    CD = 'cd'


class ServerStatus(str, Enum):
    '''Статус сервера'''
    INSTALLING = 'installing'
    SOFTWARE_INSTALL = 'software_install'
    REINSTALLING = 'reinstalling'
    ON = 'on'
    OFF = 'off'
    TURNING_ON = 'turning_on'
    TURNING_OFF = 'turning_off'
    HARD_TURNING_OFF = 'hard_turning_off'
    REBOOTING = 'rebooting'
    HARD_REBOOTING = 'hard_rebooting'
    REMOVING = 'removing'
    REMOVED = 'removed'
    CLONING = 'cloning'
    TRANSFER = 'transfer'
    BLOCKED = 'blocked'
    CONFIGURING = 'configuring'
    NO_PAID = 'no_paid'
    PERMANENT_BLOCKED = 'permanent_blocked'


class NetworkType(str, Enum):
    '''Тип сети.'''
    PUBLIC = 'public'
    LOCAL = 'local'


class NATMode(str, Enum):
    '''Тип преобразования сетевых адресов.'''
    DNAT_and_SNAT = 'dnat_and_snat'
    SNAT = 'snat'
    NO_NAT = 'no_nat'


class NetworkIPsType(str, Enum):
    '''Тип IP-адреса сети'''
    IPv4 = 'ipv4'
    IPv6 = 'ipv6'


class NetworkIPs(BaseData):
    '''Список IP-адресов сети.'''
    type: NetworkIPsType = Field(..., description='Тип IP-адреса сети')
    ip: IPv4Address | IPv6Address = Field(..., description='IP-адрес')
    ptr: str = Field(..., description='Запись имени узла')
    is_main: bool = Field(..., description='Сеть основная?')


class VDSNetwork(BaseData):
    '''Список сетей сервера.'''
    type: NetworkType = Field(..., description='Тип сети')
    nat_mode: NATMode | None = Field(
        None, description='Тип преобразования сетевых адресов.'
    )
    bandwidth: int | None = Field(None, description='Пропускная способность')
    ips: list[NetworkIPs] | None = Field(
        None, description='Список IP-адресов сети'
    )
    is_ddos_guard: bool | None = Field(
        default=None,
        description='Подключена ли DDoS-защита. Только для публичных сетей'
    )


class VDSDisk(BaseData):
    '''Список дисков сервера.'''
    id: int = Field(..., description='UID диска')
    size: int = Field(..., description='Размер в Мб')
    used: int = Field(..., description='Исполновано в Мб')
    type: str = Field(..., description='Тип диска')
    is_mounted: bool = Field(..., description='Диск смонтирован?')
    is_system: bool = Field(..., description='Диск системый?')
    system_name: str = Field(..., description='Системное имя диска')
    status: str = Field(..., description='Статус диска')


class VDS(BaseData):
    '''Модель облачного сервера'''
    id: int = Field(..., description='UID сервера')
    name: str = Field(..., description='Имя сервера')
    comment: str = Field(..., description='Комментарий')
    os: VDSOS = Field(..., description='ОС сервера')
    software: Software | None = Field(None, description='ПО из маркетплейса')
    preset_id: int | None = Field(None, description='UID тарифа')
    location: str = Field(..., description='Логация сервера')
    configurator_id: int | None = Field(
        None, description='UID конфигуратора сервера'
    )
    boot_mode: BootMode = Field(
        ..., description='Режим загрузки ОС сервера'
    )
    status: ServerStatus = Field(..., description='Статус сервера')
    start_at: datetime | None = Field(
        None, description='Дата-время запуска сервера'
    )
    is_ddos_guard: bool = Field(..., description='Защита от DDOS включена?')
    cpu: int = Field(..., description='Кол-во ядер у CPU')
    cpu_frequency: str = Field(..., description='Частота ядер CPU')
    ram: int = Field(..., description='Размер RAM в Мб')
    avatar_id: str | None = Field(None, description='UID аватара')
    vnc_pass: str = Field(None, description='Пароль от VNC')
    networks: list[VDSNetwork] = Field(...,
                                       description='Список сетей сервера.')
    disks: list[VDSDisk] = Field(..., description='Список дисков сервера.')
    created_at: datetime = Field(..., description='Дата создания сервера.')


class VDSArray(ResponseWithMeta):
    '''Ответ со списком серверов'''
    servers: list[VDS] = Field(..., description='Список серверов')


class VDSResponse(BaseResponse):
    '''Ответ с сервером'''
    server: VDS = Field(..., description='Облачный сервер')
