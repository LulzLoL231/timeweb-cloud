# -*- coding: utf-8 -*-
'''Модели для работы с почтой'''
from ..base import ResponseWithMeta, BaseResponse, BaseData


class MailboxAutoReply(BaseData):
    '''Модель автоответчика почтового ящика на входящие письма'''
    is_enabled: bool
    message: str
    subject: str


class MailboxSpamFilter(BaseData):
    '''Модель спам-фильтра почтового ящика'''
    is_enabled: bool
    action: str
    forward_to: str
    white_list: list[str]


class MailboxForwardingIncoming(BaseData):
    '''Модель пересылки входящих писем почтового ящика'''
    is_enabled: bool
    is_delete_messages: bool
    incoming_list: list[str]


class MailboxForwardingOutgoing(BaseData):
    '''Модель пересылки исходящих писем почтового ящика'''
    is_enabled: bool
    outgoing_to: str


class Mailbox(BaseData):
    '''Модель почтового ящика'''
    auto_reply: MailboxAutoReply
    spam_filter: MailboxSpamFilter
    forwarding_incoming: MailboxForwardingIncoming
    forwarding_outgoing: MailboxForwardingOutgoing
    comment: str
    fqdn: str
    mailbox: str
    password: str
    usage_space: int
    is_webmail: bool
    idn_name: str
    is_dovecot: bool


class Quota(BaseData):
    '''Модель почтовой квоты'''
    total: int
    used: int


class DomainInfo(BaseData):
    '''Модель почтовой информации о домене'''
    email: str
    used: int


class MailboxesResponse(ResponseWithMeta):
    '''Ответ со списком почтовых ящиков'''
    mailboxes: list[Mailbox]


class QuotaResponse(BaseResponse):
    '''Ответ с почтовой квотой'''
    quota: Quota


class MailboxResponse(BaseResponse):
    '''Ответ с почтовым ящиком'''
    mailbox: Mailbox


class DomainInfoResponse(BaseResponse):
    '''Ответ с почтовой информацией о домене'''
    domain_info: DomainInfo
