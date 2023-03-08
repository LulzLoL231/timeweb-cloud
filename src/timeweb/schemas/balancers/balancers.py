# -*- coding: utf-8 -*-
'''Модели для работы с балансировщиками'''
from enum import Enum
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData, BaseDelete


class Protocol(str, Enum):
    '''Протокол балансировщика

    Attributes:
        HTTP2 (str): http2
        HTTP (str): http
        HTTPS (str): https
        TCP (str): tcp
    '''
    HTTP2 = 'http2'
    HTTP = 'http'
    HTTPS = 'https'
    TCP = 'tcp'


class BalancerAlgorithm(str, Enum):
    '''Алгоритм балансировки

    Attributes:
        ROUND_ROBIN (str): roundrobin
        LEAST_CONNECTIONS (str): leastconn
    '''
    ROUND_ROBIN = 'roundrobin'
    LEAST_CONNECTIONS = 'leastconn'


class BalancerStatus(str, Enum):
    '''Статус балансировщика

    Attributes:
        STARTED (str): started
        STOPED (str): stoped
        STARTING (str): starting
        NO_PAID (str): no_paid
    '''
    STARTED = 'started'
    STOPED = 'stoped'
    STARTING = 'starting'
    NO_PAID = 'no_paid'


class BalancerRule(BaseData):
    '''Правило балансировщика

    Attributes:
        id (int): UID правила
        balancer_proto (Protocol): Протокол балансировщика
        balancer_port (int): Порт балансировщика
        server_proto (Protocol): Протокол сервера
        server_port (int): Порт сервера
    '''
    id: int = Field(..., description='UID правила')
    balancer_proto: Protocol = Field(...,
                                     description='Протокол балансировщика')
    balancer_port: int = Field(..., description='Порт балансировщика')
    server_proto: Protocol = Field(..., description='Протокол сервера')
    server_port: int = Field(..., description='Порт сервера')


class Balancer(BaseData):
    '''Балансировщик

    Attributes:
        id (int): UID балансировщика
        algo (BalancerAlgorithm): Алгоритм переключений балансировщика.
        created_at (datetime): Дата создания балансировщика.
        fall (int): Порог количества ошибок.
        inter (int): Интервал проверки.
        ip (IPv4Address | None): IP адрес балансировщика.
        local_ip (IPv4Address | None): Локальный IP адрес балансировщика.
        is_keepalive (bool): Выдает ли балансировщик сигнал о проверке жизнеспособности.
        name (str): Название балансировщика.
        path (str): Адрес балансировщика.
        proto (Protocol): Протокол балансировщика.
        rise (int): Порог количества успешных проверок.
        preset_id (int): UID тарифа балансировщика.
        is_ssl (bool): Требуется ли перенаправление на SSL.
        status (BalancerStatus): Статус балансировщика.
        is_sticky (bool): Сохраняется ли сессия.
        timeout (int): Таймаут ответа балансировщика.
        is_use_proxy (bool): Выступает ли балансировщик в качестве прокси.
        ips (list[str | IPv4Address | IPv6Address]): Список IP адресов, привязанных к балансировщику.
        rules (list[BalancerRule]): Список правил балансировщика.
    '''
    id: int = Field(..., description='UID балансировщика')
    algo: BalancerAlgorithm = Field(
        ..., description='Алгоритм переключений балансировщика.'
    )
    created_at: datetime = Field(
        ..., description='Дата создания балансировщика.'
    )
    fall: int = Field(..., description='Порог количества ошибок.')
    inter: int = Field(..., description='Интервал проверки.')
    ip: IPv4Address | None = Field(
        None, description='IP адрес балансировщика.'
    )
    local_ip: IPv4Address | None = Field(
        None, description='Локальный IP адрес балансировщика.'
    )
    is_keepalive: bool = Field(
        ..., description='Выдает ли балансировщик сигнал о проверке жизнеспособности.'
    )
    name: str = Field(..., description='Название балансировщика.')
    path: str = Field(..., description='Адрес балансировщика.')
    proto: Protocol = Field(..., description='Протокол балансировщика.')
    rise: int = Field(..., description='Порог количества успешных проверок.')
    preset_id: int = Field(..., description='UID тарифа балансировщика.')
    is_ssl: bool = Field(...,
                         description='Требуется ли перенаправление на SSL.')
    status: BalancerStatus = Field(..., description='Статус балансировщика.')
    is_sticky: bool = Field(..., description='Сохраняется ли сессия.')
    timeout: int = Field(..., description='Таймаут ответа балансировщика.')
    is_use_proxy: bool = Field(
        ..., description='Выступает ли балансировщик в качестве прокси.'
    )
    ips: list[str | IPv4Address | IPv6Address] = Field(  # В докуменатции точно не указан тип, опираемся на название.
        ..., description='Список IP адресов, привязанных к балансировщику.'
    )
    rules: list[BalancerRule] = Field(
        ..., description='Список правил балансировщика.'
    )


class BalancerResponse(BaseResponse):
    '''Ответ с балансировщиком

    Attributes:
        balancer (Balancer): Балансировщик
    '''
    balancer: Balancer = Field(..., description='Балансировщик.')


class BalancersResponse(ResponseWithMeta):
    '''Ответ со списком балансировщиков

    Attributes:
        balancers (list[Balancer]): Список балансировщиков.
    '''
    balancers: list[Balancer] = Field(...,
                                      description='Список балансировщиков.')


class BalancerRuleResponse(BaseResponse):
    '''Ответ с правилом балансировщика

    Attributes:
        rule (BalancerRule): Правило балансировщика.
    '''
    rule: BalancerRule = Field(..., description='Правило балансировщика.')


class BalancerRulesResponse(ResponseWithMeta):
    '''Ответ со списком правил балансировщика

    Attributes:
        rules (list[BalancerRule]): Список правил балансировщика.
    '''
    rules: list[BalancerRule] = Field(...,
                                      description='Список правил балансировщика.')


class BalancerIPsResponse(ResponseWithMeta):
    '''Ответ со списком IP адресов балансировщика

    Attributes:
        ips (list[str | IPv4Address | IPv6Address]): Список IP адресов балансировщика.
    '''
    ips: list[str | IPv4Address | IPv6Address] = Field(..., description='Список IP адресов балансировщика.')


class BalancerDelete(BaseResponse):
    '''Ответ с хэшом для подтверждения удаления балансировщика

    Attributes:
        balancer_delete (BaseDelete): Хэщ для подтверждения удаления балансировщика'''
    balancer_delete: BaseDelete
