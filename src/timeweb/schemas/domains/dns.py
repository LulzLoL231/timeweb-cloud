# -*- coding: utf-8 -*-
'''Модели для работы с DNS доменов.'''
from ..base import ResponseWithMeta, BaseResponse, BaseData


class DNSData(BaseData):
    '''Модель DNS данных'''
    value: str
    priority: int | None = None
    subdomain: str | None = None


class DNSRecord(BaseData):
    '''Модель DNS записи'''
    type: str
    data: DNSData
    id: int | None = None


class DNSRecordsResponse(ResponseWithMeta):
    '''Ответ со списком DNS записей'''
    dns_records: list[DNSRecord]


class DNSRecordResponse(BaseResponse):
    '''Ответ с DNS записью'''
    dns_record: DNSRecord
