# -*- coding: utf-8 -*-
'''Методы API для работы с доменами.

В Timeweb Cloud доступна регистрация и продление доменов более чем в 350 зонах.

Документация: https://timeweb.cloud/api-docs#tag/Domeny'''
import logging
from ipaddress import IPv4Address, IPv6Address

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas.time_utils import Period
from ..schemas import domains as schemas


IPAddress = IPv4Address | IPv6Address


class DomainsAPI(BaseAsyncClient):
    '''Клиент для работы с API доменов'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_domains(
        self, limit: int = 100, offset: int = 0,
        idn_name: str | None = None, sort: str | None = None,
        linked_ip: IPAddress | str | None = None,
        order: str | None = None
    ) -> schemas.DomainsResponse:
        params: dict[str, str | int] = {
            'limit': limit,
            'offset': offset
        }
        if idn_name:
            params['idn_name'] = idn_name
        if sort:
            params['sort'] = sort
        if linked_ip:
            params['linked_ip'] = str(linked_ip)
        if order:
            params['order'] = order
        domains = await self._request(
            'GET', '/domains', params=params
        )
        return schemas.DomainsResponse(**domains.json())

    async def get_domain(self, fqdn: str) -> schemas.DomainResponse:
        '''Получить информацию о домене.

        Args:
            fqdn (str): FQDN домена.

        Returns:
            schemas.DomainResponse: Информация о домене.
        '''
        domain = await self._request(
            'GET', f'/domains/{fqdn}'
        )
        return schemas.DomainResponse(**domain.json())

    async def turn_domain_autoprolong(
        self, fqdn: str, linked_ip: IPAddress | str | None = None,
        is_autoprolong_enabled: bool | None = None
    ) -> schemas.DomainResponse:
        '''Включить/выключить автопродление домена.

        Args:
            fqdn (str): FQDN домена.
            linked_ip (IPAddress | str | None, optional): Привязанный к домену IP-адрес. Defaults to None.
            is_autoprolong_enabled (bool | None, optional): Включить автопродление. Defaults to None.

        Returns:
            schemas.DomainResponse: Обновленный домен.
        '''
        data: dict[str, str | bool] = {}
        if linked_ip:
            data['linked_ip'] = str(linked_ip)
        if is_autoprolong_enabled:
            data['is_autoprolong_enabled'] = is_autoprolong_enabled
        domain = await self._request(
            'PATCH', f'/domains/{fqdn}', json=data
        )
        return schemas.DomainResponse(**domain.json())

    async def delete_domain(self, fqdn: str) -> bool:
        '''Удалить домен.

        Args:
            fqdn (str): FQDN домена.

        Returns:
            bool: Домен удалён?
        '''
        status = await self._request(
            'DELETE', f'/domains/{fqdn}'
        )
        return status.is_success

    async def get_dns_records(
        self, fqdn: str, limit: int = 100, offset: int = 0
    ) -> schemas.DNSRecordsResponse:
        '''Получить пользовательские DNS-записи домена или поддомена.

        Args:
            fqdn (str): FQDN домена или поддомена.
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Сдвиг. Defaults to 0.

        Returns:
            schemas.DNSRecordsResponse: Список DNS-записей.
        '''
        params = {
            'limit': limit,
            'offset': offset
        }
        records = await self._request(
            'GET', f'/domains/{fqdn}/dns-records', params=params
        )
        return schemas.DNSRecordsResponse(**records.json())

    async def add_dns_record(
        self, fqdn: str, type: str, value: str,
        priority: int | None = None, subdomain: str | None = None
    ) -> schemas.DNSRecordResponse:
        '''Добавить DNS-запись для домена или поддомена.

        Args:
            fqdn (str): FQDN домена или поддомена.
            type (str): Тип записи.
            value (str): Значение записи.
            priority (int | None, optional): Приоритет записи. Defaults to None.
            subdomain (str | None, optional): Полное имя поддомена. Defaults to None.

        Returns:
            schemas.DNSRecordResponse: DNS-запись.
        '''
        data: dict[str, str | int] = {
            'type': type,
            'value': value
        }
        if priority:
            data['priority'] = priority
        if subdomain:
            data['subdomain'] = subdomain
        record = await self._request(
            'POST', f'/domains/{fqdn}/dns-records', json=data
        )
        return schemas.DNSRecordResponse(**record.json())

    async def update_dns_record(
        self, fqdn: str, record_id: int, type: str, value: str,
        priority: int | None = None, subdomain: str | None = None
    ) -> schemas.DNSRecordResponse:
        '''Обновить информацию о DNS-записи домена или поддомена.

        Args:
            fqdn (str): FQDN домена или поддомена.
            record_id (int): UID DNS-записи.
            type (str): Тип записи.
            value (str): Значение записи.
            priority (int | None, optional): Приоритет записи.. Defaults to None.
            subdomain (str | None, optional): Полное имя поддомена. Defaults to None.

        Returns:
            schemas.DNSRecordResponse: DNS-запись.
        '''
        data: dict[str, str | int] = {
            'type': type,
            'value': value
        }
        if priority:
            data['priority'] = priority
        if subdomain:
            data['subdomain'] = subdomain
        record = await self._request(
            'PATCH', f'/domains/{fqdn}/dns-records/{record_id}', json=data
        )
        return schemas.DNSRecordResponse(**record.json())

    async def delete_dns_record(self, fqdn: str, record_id: int) -> bool:
        '''Удалить информацию о DNS-записи для домена или поддомена.

        Args:
            fqdn (str): FQDN домена или поддомена.
            record_id (int): UID DNS-записи.

        Returns:
            bool: Запись удалена?
        '''
        status = await self._request(
            'DELETE', f'/domains/{fqdn}/dns-records/{record_id}'
        )
        return status.is_success

    async def get_default_dns_records(
        self, fqdn: str, limit: int = 100, offset: int = 0
    ) -> schemas.DNSRecordsResponse:
        '''Получить обо всех DNS-записях по умолчанию для домена или поддомена.

        Args:
            fqdn (str): FQDN домена или поддомена.
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Сдвиг. Defaults to 0.

        Returns:
            schemas.DNSRecordsResponse: Список DNS-записей.
        '''
        params = {
            'limit': limit,
            'offset': offset
        }
        records = await self._request(
            'GET', f'/domains/{fqdn}/default-dns-records', params=params
        )
        return schemas.DNSRecordsResponse(**records.json())

    async def add_domain_subdomain(
        self, fqdn: str, subdomain_fqdn: str
    ) -> schemas.SubdomainResponse:
        '''Добавить поддомен для домена.

        Args:
            fqdn (str): FQDN домена.
            subdomain_fqdn (str): FQDN поддомена.

        Returns:
            schemas.SubdomainResponse: Поддомен.
        '''
        subdomain = await self._request(
            'POST', f'/domains/{fqdn}/subdomains/{subdomain_fqdn}'
        )
        return schemas.SubdomainResponse(**subdomain.json())

    async def delete_domain_subdomain(
        self, fqdn: str, subdomain_fqdn: str
    ) -> bool:
        '''Удалить поддомен домена.

        Args:
            fqdn (str): FQDN домена.
            subdomain_fqdn (str): FQDN поддомена.

        Returns:
            bool: Поддомен удалён?
        '''
        status = await self._request(
            'DELETE', f'/domains/{fqdn}/subdomains/{subdomain_fqdn}'
        )
        return status.is_success

    async def get_domain_ns(self, fqdn: str) -> schemas.NameServersResponse:
        '''Получить список name-серверов домена.

        Args:
            fqdn (str): FQDN домена.

        Returns:
            schemas.NameServersResponse: Список name-серверов.
        '''
        ns = await self._request(
            'GET', f'/domains/{fqdn}/name-servers'
        )
        return schemas.NameServersResponse(**ns.json())

    async def update_domain_ns(
        self, fqdn: str, name_servers: list[dict[str, str | list[IPAddress | str]]]
    ) -> schemas.NameServersResponse:
        '''Изменить name-серверы домена.

        Args:
            fqdn (str): FQDN домена.
            name_servers (list[dict[str, str  |  list[IPAddress  |  str]]]): Список name-серверов.

        Returns:
            schemas.NameServersResponse: Новые name-сервера.
        '''
        data: dict[str, list[dict[str, str | list[IPAddress | str]]]] = {
            'name_servers': []
        }
        # TODO: Мне всё ещё не нравится такая валидация, хоть она и работает как надо.
        if not isinstance(name_servers, list):
            raise ValueError('"name_servers" должен быть списком!')
        else:
            if len(name_servers) == 0:
                raise ValueError(
                    '"name_servers" должен быть не пустым списком.')
            else:
                for idx, server in enumerate(name_servers):
                    if not isinstance(server, dict):
                        raise ValueError(
                            f'Объект #{idx} "name_servers" должен быть словарём!'
                        )
                    else:
                        data['name_servers'].append(server)
        ns = await self._request(
            'PUT', f'/domains/{fqdn}/name-servers', json=data
        )
        return schemas.NameServersResponse(**ns.json())

    async def get_domains_requests(
        self, person_id: int | None = None
    ) -> schemas.DomainsRequestsResponse:
        '''Получить список заявок доменов.

        Args:
            person_id (int | None, optional): UID администратора домена. Defaults to None.

        Returns:
            schemas.DomainsRequestsResponse: Список заявок.
        '''
        params: dict[str, int] = {}
        if person_id:
            params['person_id'] = person_id
        requests = await self._request(
            'GET', '/domains-requests', params=params
        )
        return schemas.DomainsRequestsResponse(**requests.json())

    async def create_domain_register_request(
        self, fqdn: str, person_id: int, period: Period | str | None = None,
        is_autoprolong_enabled: bool | None = None,
        is_whois_privacy_enabled: bool | None = None,
        ns: list[dict[str, str | list[IPAddress | str]]] | None = None
    ) -> schemas.DomainRequestResponse:
        '''Создать заявку на регистрацию домена.

        Args:
            fqdn (str): FQDN домена.
            person_id (int): UID администратора домена.
            period (Period | str | None, optional): Период оплаты. Defaults to None.
            is_autoprolong_enabled (bool | None, optional): Включить автопродление. Defaults to None.
            is_whois_privacy_enabled (bool | None, optional): Включить скрытие данных админа. Defaults to None.
            ns (list[dict[str, str  |  list[IPAddress  |  str]]] | None, optional): Список name-серверов. Defaults to None.

        Note:
            `ns` должен иметь список как минимум из 2-х значений.

        Returns:
            schemas.DomainRequestResponse: Заявка на регистрацию.
        '''
        data = {
            'action': 'register',
            'fqdn': fqdn,
            'person_id': person_id
        }
        if ns:
            if len(ns) < 2:
                raise ValueError('"ns" должно иметь как минимум 2 значения!')
            data['ns'] = ns
        if period:
            data['period'] = str(period)
        if is_autoprolong_enabled:
            data['is_autoprolong_enabled'] = is_autoprolong_enabled
        if is_whois_privacy_enabled:
            data['is_whois_privacy_enabled'] = is_whois_privacy_enabled
        request = await self._request(
            'POST', '/domains-requests', json=data
        )
        return schemas.DomainRequestResponse(**request.json())

    async def create_domain_transfer_request(
        self, fqdn: str, auth_code: str
    ) -> schemas.DomainRequestResponse:
        '''Создать заявку на трансфер домена.

        Args:
            fqdn (str): FQDN домена.
            auth_code (str): Код авторизации для переноса домена.

        Returns:
            schemas.DomainRequestResponse: Заявка на трансфер.
        '''
        data = {
            'action': 'transfer',
            'fqdn': fqdn,
            'auth_code': auth_code
        }
        request = await self._request(
            'POST', '/domains-requests', json=data
        )
        return schemas.DomainRequestResponse(**request.json())

    async def create_domain_prolong_request(
        self, fqdn: str, is_antispam_enabled: bool | None = None,
        is_autoprolong_enabled: bool | None = None,
        is_whois_privacy_enabled: bool | None = None,
        period: Period | str | None = None,
        person_id: int | None = None, prime: str | None = None
    ) -> schemas.DomainRequestResponse:
        '''Создать заявку на продление домена.

        Args:
            fqdn (str): FQDN домена.
            is_antispam_enabled (bool | None, optional): Услуга "Антиспам" включена. Defaults to None.
            is_autoprolong_enabled (bool | None, optional): Автопродление включено. Defaults to None.
            is_whois_privacy_enabled (bool | None, optional): Скрытие данных администратора включено. Defaults to None.
            period (Period | str | None, optional): Период оплаты. Defaults to None.
            person_id (int | None, optional): UID администратора домена. Defaults to None.
            prime (str | None, optional): Тип прайма домена. Defaults to None.

        Returns:
            schemas.DomainRequestResponse: Заявка на продление.
        '''
        data: dict[str, str | int | bool] = {
            'fqdn': fqdn
        }
        if is_antispam_enabled:
            data['is_antispam_enabled'] = is_antispam_enabled
        if is_autoprolong_enabled:
            data['is_autoprolong_enabled'] = is_autoprolong_enabled
        if is_whois_privacy_enabled:
            data['is_whois_privacy_enabled'] = is_whois_privacy_enabled
        if period:
            data['period'] = str(period)
        if person_id:
            data['person_id'] = person_id
        if prime:
            data['prime'] = prime
        request = await self._request(
            'POST', '/domains-requests', json=data
        )
        return schemas.DomainRequestResponse(**request.json())

    async def get_domain_request(self, request_id: int) -> schemas.DomainRequestResponse:
        '''Получить информацию о заявке к домену.

        Args:
            request_id (int): UID заявки.

        Returns:
            schemas.DomainRequestResponse: Информация о заявке к домену.
        '''
        request = await self._request(
            'GET', f'/domains-requests/{request_id}'
        )
        return schemas.DomainRequestResponse(**request.json())

    async def pay_domain_request(
        self, request_id: int, money_source: str,
        person_id: int | None = None, payment_type: str | None = None,
        payer_id: int | None = None, bonus_id: int | None = None
    ) -> schemas.DomainRequestResponse:
        '''Оплата заявки домена.

        Args:
            request_id (int): UID заявки.
            money_source (str): Способ оплаты.
            person_id (int | None, optional): UID администратора домена. Defaults to None.
            payment_type (str | None, optional): Тип платёжной системы. Defaults to None.
            payer_id (int | None, optional): UID номера плательщика. Defaults to None.
            bonus_id (int | None, optional): UID бонуса. Defaults to None.

        Note:
            `money_source` может быть: `use`, `invoice`, `bonus`.

            При `money_source` = `invoice` - `payment_type` и `payer_id` становятся обязательными.

            При `money_source` = `bonus` - `bonus_id` становится обязательным.

        References:
            https://timeweb.cloud/api-docs#tag/Domeny/paths/~1api~1v1~1domains-requests~1%7Brequest_id%7D/patch

        Raises:
            NameError: если не указан обязательная переменная.

        Returns:
            schemas.DomainRequestResponse: Обновлённая заявка.
        '''
        if money_source == 'invoice':
            if not payment_type:
                raise NameError('"payment_type" обязательный аргумент!')
            if not payer_id:
                raise NameError('"payer_id" обязательный аргумент!')
        elif money_source == 'bonus':
            if not bonus_id:
                raise NameError('"bonus_id" обязательный аргумент!')
        data: dict[str, str | int] = {
            'money_source': money_source
        }
        if payer_id:
            data['payer_id'] = payer_id
        if payment_type:
            data['payment_type'] = payment_type
        if bonus_id:
            data['bonus_id'] = bonus_id
        if person_id:
            data['person_id'] = person_id
        request = await self._request(
            'PATCH', f'/domains-requests/{request_id}', json=data
        )
        return schemas.DomainRequestResponse(**request.json())

    async def update_domain_transfer_request(
        self, request_id: int, auth_code: str,
        person_id: int | None = None
    ) -> schemas.DomainRequestResponse:
        '''Обнавить заявку на трансфер домена.

        Args:
            request_id (int): UID заявки.
            auth_code (str): Код авторизации для переноса домена.
            person_id (int | None, optional): UID администратора домена. Defaults to None.

        Returns:
            schemas.DomainRequestResponse: Обновлённая заявка.
        '''
        data: dict[str, str | int] = {
            'auth_code': auth_code,
            'money_source': 'free'
        }
        if person_id:
            data['person_id'] = person_id
        request = await self._request(
            'PATCH', f'/domains-requests/{request_id}', json=data
        )
        return schemas.DomainRequestResponse(**request.json())

    async def get_tlds(
        self, is_published: bool | None = None,
        is_registered: bool | None = None
    ) -> schemas.TLDomainsResponse:
        '''Получить информацию о доменных зонах.

        Args:
            is_published (bool | None, optional): Доменная зона опубликована. Defaults to None.
            is_registered (bool | None, optional): Доменная зона зарегистрирована. Defaults to None.

        Returns:
            schemas.TLDomainsResponse: Список доменных зон.
        '''
        params: dict[str, bool] = {}
        if is_published:
            params['is_published'] = is_published
        if is_registered:
            params['is_registered'] = is_registered
        tlds = await self._request(
            'GET', '/tlds', params=params
        )
        return schemas.TLDomainsResponse(**tlds.json())

    async def get_tld(self, tld_id: int) -> schemas.TLDomainResponse:
        '''Получить информацию о доменной зоне.

        Args:
            tld_id (int): UID доменной зоны.

        Returns:
            schemas.TLDomainResponse: Информация о доменной зоне.
        '''
        tld = await self._request(
            'GET', f'/tlds/{tld_id}'
        )
        return schemas.TLDomainResponse(**tld.json())

    async def check_domain(self, fqdn: str) -> schemas.DomainAvailability:
        '''Проверить, доступен ли домен для регистрации.

        Args:
            fqdn (str): FQDN домена.

        Returns:
            schemas.DomainAvailability: Информация о доступности домена.
        '''
        status = await self._request(
            'GET', f'/check-domain/{fqdn}'
        )
        return schemas.DomainAvailability(**status.json())

    async def add_domain(self, fqdn: str) -> bool:
        '''Добавить домен в аккаунт.

        Args:
            fqdn (str): FQDN домена.

        Returns:
            bool: Домен добавлен?
        '''
        status = await self._request(
            'POST', f'/add-domain/{fqdn}'
        )
        return status.is_success
