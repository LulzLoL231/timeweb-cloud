# -*- coding: utf-8 -*-
'''Методы API для работы с почтой.

В Timeweb Cloud доступна инфраструктура готовых почтовых серверов.
Вы можете создавать и настраивать неограниченное число ящиков на своих доменах.

Документация: https://timeweb.cloud/api-docs#tag/Pochta'''
import logging

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import mail as schemas


class MailAPI(BaseAsyncClient):
    '''Клиент для работы с API почты'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_mailboxes(
        self, limit: int = 100, offset: int = 0, search: str | None = None
    ) -> schemas.MailboxesResponse:
        '''Получить список почтовых ящиков.

        Args:
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Сдвиг. Defaults to 0.
            search (str | None, optional): Поиск почтового ящика по названию. Defaults to None.

        Returns:
            schemas.MailboxesResponse: Список почтовых ящиков.
        '''
        params: dict[str, str | int] = {
            'limit': limit,
            'offset': offset
        }
        if search:
            params['search'] = search
        mailboxes = await self._request(
            'GET', '/mail', params=params
        )
        return schemas.MailboxesResponse(**mailboxes.json())

    async def get_quota(self) -> schemas.QuotaResponse:
        '''Получить квоту почты аккаунта.

        Returns:
            schemas.QuotaResponse: Квота почты.
        '''
        quota = await self._request(
            'GET', '/mail/quota'
        )
        return schemas.QuotaResponse(**quota.json())

    async def change_quota(self, total: int | None = None) -> schemas.QuotaResponse:
        '''Изменить информацию о квоте почты аккаунта.

        Args:
            total (int | None, optional): Общее кол-во места на почте. Defaults to None.

        Returns:
            schemas.QuotaResponse: Обновлённая квота.
        '''
        data: dict[str, int] = {}
        if total:
            data['total'] = total
        updated = await self._request(
            'PATCH', '/mail/quota', json=data
        )
        return schemas.QuotaResponse(**updated.json())

    async def get_domain_mailboxes(
        self, domain: str, limit: int = 100, offset: int = 0,
        search: str | None = None
    ) -> schemas.MailboxesResponse:
        '''Получить список почтовых ящиков домена.

        Args:
            domain (str): FQDN домена.
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Сдвиг. Defaults to 0.
            search (str | None, optional): Поиск почтового ящика по названию. Defaults to None.

        Returns:
            schemas.MailboxesResponse: Список почтовых ящиков.
        '''
        params: dict[str, str | int] = {
            'limit': limit,
            'offset': offset
        }
        if search:
            params['search'] = search
        mailboxes = await self._request(
            'GET', f'/mail/{domain}', params=params
        )
        return schemas.MailboxesResponse(**mailboxes.json())

    async def create_mailbox(
        self, domain: str, mailbox: str, password: str,
        comment: str | None = None
    ) -> schemas.MailboxResponse:
        '''Создать почтовый ящик.

        Args:
            domain (str): FQDN домена.
            mailbox (str): Название почтового ящика.
            password (str): Пароль почтового ящика.
            comment (str | None, optional): Комментарий почтового ящика. Defaults to None.

        Returns:
            schemas.MailboxResponse: Созданный почтовый ящик.
        '''
        data = {
            'mailbox': mailbox,
            'password': password
        }
        if comment:
            data['comment'] = comment
        new = await self._request(
            'POST', f'/mail/domains/{domain}',
            json=data
        )
        return schemas.MailboxResponse(**new.json())

    async def get_domain_info(self, domain: str) -> schemas.DomainInfoResponse:
        '''получение почтовой информации о домене.

        Args:
            domain (str): FQDN домена.

        Returns:
            schemas.DomainInfoResponse: Почтовая информация о домене.
        '''
        info = await self._request(
            'GET', f'/mail/domains/{domain}/info'
        )
        return schemas.DomainInfoResponse(**info.json())

    async def change_domain_info(
        self, domain: str, email: str | None = None
    ) -> schemas.DomainInfoResponse:
        '''Изменить почтовую информацию о домене.

        Args:
            domain (str): FQDB домена.
            email (str | None, optional): Адрес для сбора почты с ошибочных ящиков. Defaults to None.

        Returns:
            schemas.DomainInfoResponse: Обновленная почтовая информация.
        '''
        data: dict[str, str] = {}
        if email:
            data['email'] = email
        updated = await self._request(
            'PATCH', f'/mail/domains/{domain}/info',
            json=data
        )
        return schemas.DomainInfoResponse(**updated.json())

    async def get_mailbox(
        self, domain: str, mailbox: str
    ) -> schemas.MailboxResponse:
        '''Получение почтового ящика.

        Args:
            domain (str): FQDN домена.
            mailbox (str): Название почтового ящика.

        Returns:
            schemas.MailboxResponse: Почтовый ящик.
        '''
        box = await self._request(
            'GET', f'/mail/domains/{domain}/mailboxes/{mailbox}'
        )
        return schemas.MailboxResponse(**box.json())

    async def change_mailbox(
        self, domain: str, mailbox: str,
        comment: str | None = None, password: str | None = None,
        auto_reply: dict[str, bool | str] | None = None,
        spam_filter: dict[str, bool | str | list[str]] | None = None,
        forwarding_incoming: dict[str, bool | str | list[str]] | None = None,
        forwarding_outgoing: dict[str, bool | str] | None = None
    ) -> schemas.MailboxResponse:
        '''Изменить почтовый ящик.

        Args:
            domain (str): FQDN домена.
            mailbox (str): Название почтового ящика.
            comment (str | None, optional): Комментарий. Defaults to None.
            password (str | None, optional): Пароль. Defaults to None.
            auto_reply (dict[str, bool  |  str] | None, optional): Автоответчик. Defaults to None.
            spam_filter (dict[str, bool  |  str  |  list[str]] | None, optional): Спам-фильтр. Defaults to None.
            forwarding_incoming (dict[str, bool  |  str  |  list[str]] | None, optional): Пересылка входящий писем. Defaults to None.
            forwarding_outgoing (dict[str, bool  |  str] | None, optional): Пересылка исходящих писем. Defaults to None.

        References:
            https://timeweb.cloud/api-docs#tag/Pochta/paths/~1api~1v1~1mail~1domains~1%7Bdomain%7D~1mailboxes~1%7Bmailbox%7D/patch

        Returns:
            schemas.MailboxResponse: Обновлённый почтовый ящик.
        '''
        data: dict[str, str | dict[str, bool | str] | dict[str, bool | str | list[str]]] = {}
        if auto_reply:
            data['auto_reply'] = auto_reply
        if spam_filter:
            data['spam_filter'] = spam_filter
        if forwarding_incoming:
            data['forwarding_incoming'] = forwarding_incoming
        if forwarding_outgoing:
            data['forwarding_outgoing'] = forwarding_outgoing
        if comment:
            data['comment'] = comment
        if password:
            data['password'] = password
        updated = await self._request(
            'PATCH', f'/mail/domains/{domain}/mailboxes/{mailbox}',
            json=data
        )
        return schemas.MailboxResponse(**updated.json())

    async def delete_mailbox(self, domain: str, mailbox: str) -> bool:
        '''Удалить почтовый ящик.

        Args:
            domain (str): FQDN домена.
            mailbox (str): Название почтового ящика.

        Returns:
            bool: Почтовый ящик удалён?
        '''
        status = await self._request(
            'DELETE', f'/mail/domains/{domain}/mailboxes/{mailbox}'
        )
        return status.is_success
