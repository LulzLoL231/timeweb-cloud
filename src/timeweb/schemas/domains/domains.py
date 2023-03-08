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
    '''Модель допустимых периодов продления доменов.

    Attributes:
        period (Period): Период оплаты (Для доменов в зонах .ru и .рф только 1-3 года).
        price (Decimal): Стоимость домена за указанный период.
    '''
    period: Period
    price: Decimal


class Subdomain(BaseData):
    '''Модель данных поддомена.

    Attributes:
        fqdn (str): Полное имя поддомена.
        id (int): Уникальный идентификатор поддомена.
        linked_ip (IPAddress | None): Привязанный к поддомену IP-адрес.
    '''
    fqdn: str
    id: int
    linked_ip: IPAddress | None


class Domain(BaseData):
    '''Модель данных домена.

    Attributes:
        days_left (int): Количество дней, оставшихся до конца срока регистрации домена.
        allowed_buy_periods (list[DomainAllowedBuyPeriods]): Допустимые периоды продления домена.
        domain_status (str): Статус домена.
        expiration (datetime | str): Дата окончания срока регистрации домена, для доменов без срока окончания регистрации будет приходить 0000-00-00.
        fqdn (str): Полное имя домена.
        id (int): Уникальный идентификатор домена.
        is_autoprolong_enabled (bool | None): Это логическое значение, которое показывает, включено ли автопродление домена.
        is_premium (bool): Это логическое значение, которое показывает, является ли домен премиальным.
        is_prolong_allowed (bool): Это логическое значение, которое показывает, можно ли сейчас продлить домен.
        is_technical (bool): Это логическое значение, которое показывает, является ли домен техническим.
        is_whois_privacy_enabled (bool | None): Это логическое значение, которое показывает, включено ли скрытие данных администратора домена для whois. Если приходит null, значит для данной зоны эта услуга не доступна.
        linked_ip (IPAddress | None): Привязанный к домену IP-адрес.
        paid_till (datetime | None): До какого числа оплачен домен.
        person_id (int | None): Идентификатор администратора, на которого зарегистрирован домен.
        premium_prolong_cost (Decimal | None): Стоимость премиального домена.
        provider (str | None): Идентификатор регистратора домена.
        request_status (str | None): Статус заявки на продление/регистрацию/трансфер домена.
        tld_id (int | None): Идентификатор доменной зоны.
        subdomains (list[Subdomain]): Список поддоменов.
    '''
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
    '''Ответ со списком доменов.

    Attributes:
        domains (list[Domain]): Список доменов
    '''
    domains: list[Domain]


class DomainResponse(BaseResponse):
    '''Ответ с доменом.

    Attributes:
        domain (Domain): домен
    '''
    domain: Domain


class SubdomainResponse(BaseResponse):
    '''Ответ с поддоменом.

    Attributes:
        subdomain (Subdomain): поддомен
    '''
    subdomain: Subdomain


class DomainAvailability(BaseResponse):
    '''Ответ с информацией о доступности домена для регистрации.

    Attributes:
        is_domain_available (bool): Домен доступен для регистрации?
    '''
    is_domain_available: bool
