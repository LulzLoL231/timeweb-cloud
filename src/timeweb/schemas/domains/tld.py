# -*- coding: utf-8 -*-
'''Модели для работы с доменами первого уровня.'''
from decimal import Decimal

from ..time_utils import Period
from ..base import ResponseWithMeta, BaseResponse, BaseData


class TLDAllowedBuyPeriods(BaseData):
    '''Модель допустимых периодов продления доменов.

    Attributes:
        period (Period): Период регистрации/продления домена.
        price (Decimal): Цена регистрации/продления домена.
    '''
    period: Period
    price: Decimal


class TLDomain(BaseData):
    '''Модель данных доменной зоны.

    Attributes:
        allowed_buy_periods (list[TLDAllowedBuyPeriods]): Список доступных периодов для регистрации/продления доменов со стоимостью.
        early_renew_period (int | None): Количество дней до истечение срока регистрации, когда можно продлять домен.
        grace_period (int): Количество дней, которые действует льготный период когда вы ещё можете продлить домен, после окончания его регистрации
        id (int): Идентификатор доменной зоны.
        is_published (bool): Это логическое значение, которое показывает, опубликована ли доменная зона.
        is_registered (bool): Это логическое значение, которое показывает, зарегистрирована ли доменная зона.
        is_whois_privacy_default_enabled (bool): Это логическое значение, которое показывает, включено ли по умолчанию скрытие данных администратора для доменной зоны.
        is_whois_privacy_enabled (bool): Это логическое значение, которое показывает, доступно ли управление скрытием данных администратора для доменной зоны.
        name (str): Имя доменной зоны.
        price (Decimal): Цена регистрации домена
        prolong_price (Decimal): Цена продления домена.
        registrar (str): Регистратор доменной зоны.
        transfer (Decimal): Цена услуги трансфера домена.
        whois_privacy_price (Decimal): Цена услуги скрытия данных администратора для доменной зоны.
    '''
    allowed_buy_periods: list[TLDAllowedBuyPeriods]
    early_renew_period: int | None
    grace_period: int
    id: int
    is_published: bool
    is_registered: bool
    is_whois_privacy_default_enabled: bool
    is_whois_privacy_enabled: bool
    name: str
    price: Decimal
    prolong_price: Decimal
    registrar: str
    transfer: Decimal
    whois_privacy_price: Decimal


class TLDomainsResponse(ResponseWithMeta):
    '''Ответ со списком доменных зон.

    Attributes:
        top_level_domains (list[TLDomain]): Список доменных зон
    '''
    top_level_domains: list[TLDomain]


class TLDomainResponse(BaseResponse):
    '''Ответ с доменной зоной.

    Attributes:
        top_level_domain (TLDomain): Доменная зона
    '''
    top_level_domain: TLDomain
