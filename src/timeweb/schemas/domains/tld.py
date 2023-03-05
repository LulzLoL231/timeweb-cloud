# -*- coding: utf-8 -*-
'''Модели для работы с доменами первого уровня.'''
from decimal import Decimal

from ..time_utils import Period
from ..base import ResponseWithMeta, BaseResponse, BaseData


class TLDAllowedBuyPeriods(BaseData):
    '''Модель допустимых периодов продления доменов'''
    period: Period
    price: Decimal


class TLDomain(BaseData):
    '''Модель данных доменной зоны'''
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
    '''Ответ со списком доменных зон'''
    top_level_domains: list[TLDomain]


class TLDomainResponse(BaseResponse):
    '''Ответ с доменной зоной'''
    top_level_domain: TLDomain
