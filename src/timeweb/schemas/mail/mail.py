# -*- coding: utf-8 -*-
'''Модели для работы с почтой'''
from ..base import ResponseWithMeta, BaseResponse, BaseData


class MailboxAutoReply(BaseData):
    '''Модель автоответчика почтового ящика на входящие письма.

    Attributes:
        is_enabled (bool): Включен ли автоответчик на входящие письма
        message (str): Сообщение автоответчика на входящие письма
        subject (str): Тема сообщения автоответчика на входящие письма
    '''
    is_enabled: bool
    message: str
    subject: str


class MailboxSpamFilter(BaseData):
    '''Модель спам-фильтра почтового ящика.

    Attributes:
        is_enabled (bool): Включен ли спам-фильтр
        action (str): Что делать с письмами, которые попадают в спам.
        forward_to (str): Адрес для пересылки при выбранном действии forward из параметра action
        white_list (list[str]): Белый список адресов от которых письма не будут попадать в спам
    '''
    is_enabled: bool
    action: str
    forward_to: str
    white_list: list[str]


class MailboxForwardingIncoming(BaseData):
    '''Модель пересылки входящих писем почтового ящика.

    Attributes:
        is_enabled (bool): Включена ли пересылка входящик писем
        is_delete_messages (bool): Удалять ли входящие письма
        incoming_list (list[str]): Список адресов для пересылки
    '''
    is_enabled: bool
    is_delete_messages: bool
    incoming_list: list[str]


class MailboxForwardingOutgoing(BaseData):
    '''Модель пересылки исходящих писем почтового ящика.

    Attributes:
        is_enabled (bool): Включена ли пересылка исходящих писем
        outgoing_to (str): Адрес для пересылки исходящих писем
    '''
    is_enabled: bool
    outgoing_to: str


class Mailbox(BaseData):
    '''Модель почтового ящика.

    Attributes:
        auto_reply (MailboxAutoReply): Автоответчик на входящие письма
        spam_filter (MailboxSpamFilter): Спам-фильтр
        forwarding_incoming (MailboxForwardingIncoming): Пересылка входящик писем
        forwarding_outgoing (MailboxForwardingOutgoing): Пересылка исходящих писем
        comment (str): Комментарий к почтовому ящику
        fqdn (str): Домен почты
        mailbox (str): Название почтового ящика
        password (str): Пароль почтового ящика
        usage_space (int): Использованное место на почтовом ящике (в Мб)
        is_webmail (bool): Доступен ли Webmail
        idn_name (str): IDN домен почтового ящика
        is_dovecot (bool): Есть ли доступ через dovecot
    '''
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
    '''Модель почтовой квоты.

    Attributes:
        total (int): Общее количество места на почте (в Мб.)
        used (int): Занятое место на почте (в Мб.)
    '''
    total: int
    used: int


class DomainInfo(BaseData):
    '''Модель почтовой информации о домене.

    Attributes:
        email (str): Адрес для сбора почты с ошибочных ящиков
        used (int): Использованное место на почте (в Мб.)
    '''
    email: str
    used: int


class MailboxesResponse(ResponseWithMeta):
    '''Ответ со списком почтовых ящиков.

    Attributes:
        mailboxes (list[Mailbox]): Список почтовых ящиков
    '''
    mailboxes: list[Mailbox]


class QuotaResponse(BaseResponse):
    '''Ответ с почтовой квотой.

    Attributes:
        quota (Quota): Почтовая квота
    '''
    quota: Quota


class MailboxResponse(BaseResponse):
    '''Ответ с почтовым ящиком.

    Attributes:
        mailbox (Mailbox): Почтовый ящик
    '''
    mailbox: Mailbox


class DomainInfoResponse(BaseResponse):
    '''Ответ с почтовой информацией о домене.

    Attributes:
        domain_info (DomainInfo): Почтовая информация о домене
    '''
    domain_info: DomainInfo
