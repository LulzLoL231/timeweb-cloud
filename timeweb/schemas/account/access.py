# -*- coding: utf-8 -*-
from ipaddress import IPv4Address

from pydantic import Field, BaseModel

from ..base import BaseResponse


class WhiteList(BaseModel):
    '''Список разрешенных IP адресов и стран.

    Attributes:
        ips (list[IPv4Address]): Список разрешенных IP адресов.
        countries (list[str]): Список разрешенных стран.
    '''
    ips: list[IPv4Address] = Field(
        ..., description='Список разрешенных IP адресов.'
    )
    countries: list[str] = Field(
        ..., description='Список разрешенных стран.'
    )


class AccountAccess(BaseResponse):
    '''Информация о ограничениях авторизации пользователя.

    Attributes:
        is_ip_restrictions_enabled (bool): Включены ли ограничения по IP.
        is_country_restrictions_enabled (bool): Включены ли ограничения по странам.
        white_list (WhiteList): Список разрешенных IP адресов и стран.
    '''
    is_ip_restrictions_enabled: bool = Field(
        ..., description='Включены ли ограничения по IP.'
    )
    is_country_restrictions_enabled: bool = Field(
        ..., description='Включены ли ограничения по странам.'
    )
    white_list: WhiteList = Field(
        ..., description='Список разрешенных IP адресов и стран.'
    )
