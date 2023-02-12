# -*- coding: utf-8 -*-
'''Модели для работы с балансировщиками'''
from enum import Enum
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta, BaseResponse


class Protocol(str, Enum):
    '''Протокол балансировщика'''
    HTTP2 = 'http2'
    HTTP = 'http'
    HTTPS = 'https'
    TCP = 'tcp'


class BalancerAlgorithm(str, Enum):
    '''Алгоритм балансировки'''
    ROUND_ROBIN = 'roundrobin'
    LEAST_CONNECTIONS = 'leastconn'


class BalancerStatus(str, Enum):
    '''Статус балансировщика'''
    STARTED = 'started'
    STOPED = 'stoped'
    STARTING = 'starting'
    NO_PAID = 'no_paid'


class BalancerRule(BaseModel):
    '''Правило балансировщика'''
    id: int = Field(..., description='UID правила')
    balancer_proto: Protocol = Field(..., description='Протокол балансировщика')
    balancer_port: int = Field(..., description='Порт балансировщика')
    server_proto: Protocol = Field(..., description='Протокол сервера')
    server_port: int = Field(..., description='Порт сервера')


class Balancer(BaseModel):
    '''Балансировщик'''
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
    is_ssl: bool = Field(..., description='Требуется ли перенаправление на SSL.')
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
    '''Ответ с балансировщиком'''
    balancer: Balancer = Field(..., description='Балансировщик.')


class BalancersResponse(ResponseWithMeta):
    '''Ответ со списком балансировщиков'''
    balancers: list[Balancer] = Field(..., description='Список балансировщиков.')


class BalancerRuleResponse(BaseResponse):
    '''Ответ с правилом балансировщика'''
    rule: BalancerRule = Field(..., description='Правило балансировщика.')


class BalancerRulesResponse(ResponseWithMeta):
    '''Ответ со списком правил балансировщика'''
    rules: list[BalancerRule] = Field(..., description='Список правил балансировщика.')


class BalancerIPsResponse(ResponseWithMeta):
    '''Ответ со списком IP адресов балансировщика'''
    ips: list[str | IPv4Address | IPv6Address] = Field(..., description='Список IP адресов балансировщика.')
