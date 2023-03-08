# -*- coding: utf-8 -*-
'''Модели для работы с DNS доменов.'''
from ..base import ResponseWithMeta, BaseResponse, BaseData


class DNSData(BaseData):
    '''Модель DNS данных

    Attributes:
        value (str): Значение DNS-записи.
        priority (int | None): Приоритет DNS-записи.
        subdomain (str | None): Полное имя поддомена.
    '''
    value: str
    priority: int | None = None
    subdomain: str | None = None


class DNSRecord(BaseData):
    '''Модель DNS записи

    Attributes:
        type (str): Тип DNS-записи.
        data (DNSData): Данные DNS-записи.
        id (int | None): Идентификатор DNS-записи.
    '''
    type: str
    data: DNSData
    id: int | None = None


class DNSRecordsResponse(ResponseWithMeta):
    '''Ответ со списком DNS записей

    Attributes:
        dns_records (list[DNSRecord]): Список DNS записей
    '''
    dns_records: list[DNSRecord]


class DNSRecordResponse(BaseResponse):
    '''Ответ с DNS записью

    Attributes:
        dns_record (DNSRecord): DNS запись
    '''
    dns_record: DNSRecord
