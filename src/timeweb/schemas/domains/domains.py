# -*- coding: utf-8 -*-
'''Модели для работы с доменами.'''
from decimal import Decimal
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import validator

from ..time_utils import Period
from ..base import ResponseWithMeta, BaseResponse, BaseData


IPAddress = IPv4Address | IPv6Address


class DomainAllowedBuyPeriods(BaseData):
    '''Модель допустимых периодов продления доменов'''
    period: Period
    price: Decimal


class Subdomain(BaseData):
    '''Модель данных поддомена'''
    fqdn: str
    id: int
    linked_ip: IPAddress | None


class Domain(BaseData):
    '''Модель данных домена'''
    days_left: int
    allowed_buy_periods: list[DomainAllowedBuyPeriods]
    domain_status: str
    expiration: datetime | str
    fqdn: str
    id: int
    is_autoprolong_enabled: bool | None
    is_premium: bool
    is_prolong_allowed: bool
    is_technical: bool
    is_whois_privacy_enabled: bool | None
    linked_ip: IPAddress | None
    paid_till: datetime | None
    person_id: int | None
    premium_prolong_cost: Decimal | None
    provider: str | None
    request_status: str | None
    tld_id: int | None
    subdomains: list[Subdomain]

    @validator('expiration', pre=True)
    def valid_expiration(cls, v) -> datetime | str:
        dt = v
        if isinstance(v, str):
            try:
                dt = datetime.fromisoformat(v)
            except Exception:
                dt = v
        elif isinstance(v, datetime):
            dt = v
        return dt


class DomainsResponse(ResponseWithMeta):
    '''Ответ со списком доменов'''
    domains: list[Domain]


class DomainResponse(BaseResponse):
    '''Ответ с доменом'''
    domain: Domain


class SubdomainResponse(BaseResponse):
    '''Ответ с поддоменом'''
    subdomain: Subdomain


class DomainAvailability(BaseResponse):
    '''Ответ с информацией о доступности домена для регистрации'''
    is_domain_available: bool
