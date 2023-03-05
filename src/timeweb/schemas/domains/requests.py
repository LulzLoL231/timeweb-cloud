# -*- coding: utf-8 -*-
'''Модели для работы с заявками над доменами.'''
from datetime import datetime

from ..time_utils import Period
from ..base import ResponseWithMeta, BaseResponse, BaseData


class DomainRequest(BaseData):
    '''Модель данных о заявки над доменом.'''
    account_id: str
    auth_code: str | None
    date: datetime
    domain_bundle_id: str | None
    error_code_transfer: str | None
    fqdn: str
    group_id: int
    id: int
    is_antispam_enabled: bool
    is_autoprolong_enabled: bool | None
    is_whois_privacy_enabled: bool
    message: str | None
    money_source: str | None
    period: Period
    person_id: int
    prime: str | None
    soon_expire: int
    sort_order: int
    type: str


class DomainsRequestsResponse(ResponseWithMeta):
    '''Ответ со списком заявок к доменам'''
    requests: list[DomainRequest]


class DomainRequestResponse(BaseResponse):
    '''Ответ с заявкой к домену'''
    request: DomainRequest
