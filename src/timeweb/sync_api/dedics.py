# -*- coding: utf-8 -*-
'''Методы API для работы с API выделенных серверов.

Выделенные серверы используют, когда необходимо разместить сложную нагруженную систему,
для которой недостаточно мощностей виртуального хостинга или облачного сервера.
Это может быть крупный сайт, интернет-магазин, любой ресурсоемкий проект.

Документация: https://timeweb.cloud/api-docs#tag/Vydelennye-servery'''
import json
import logging

from httpx import Client

from .base import BaseClient
from ..schemas.servers import dedics as schemas


class DedicsAPI(BaseClient):
    '''Клиент для работы с API выделенных серверов.'''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    def get_dedics(self) -> schemas.DedicatedServers:
        '''Получение списка выделенных серверов.

        Returns:
            DedicatedServers: Список выделенных серверов.
        '''
        dedics = self._request(
            'GET', '/dedicated-servers'
        )
        return schemas.DedicatedServers(**dedics.json())

    def create(
        self, plan_id: int, preset_id: int, name: str,
        payment_period: schemas.PaymentPeriods,
        os_id: int | None = None, cp_id: int | None = None,
        bandwidth_id: int | None = None, network_drive_id: int | None = None,
        additional_ip_addr_id: int | None = None, comment: str | None = None
    ) -> schemas.DedicatedServerResponse:
        '''Создание выделенного сервера.

        Args:
            plan_id (int): UID плана.
            preset_id (int): UID пресета.
            name (str): Имя выделенного сервера.
            payment_period (PaymentPeriods): Период оплаты.
            comment (str | None, optional): Комментарий. Defaults to None.
            os_id (int | None, optional): UID операционной системы. Defaults to None.
            cp_id (int | None, optional): UID панели управления. Defaults to None.
            bandwidth_id (int | None, optional): UID интернет-канала. Defaults to None.
            network_drive_id (int | None, optional): UID сетевого диска. Defaults to None.
            additional_ip_addr_id (int | None, optional): UID дополнительного IP. Defaults to None.

        Raises:
            ValueError: Если длина имени/комментария выделенного сервера больше 255 символов.

        Returns:
            DedicatedServerResponse: Ответ от API.
        '''
        if len(name) > 255:
            raise ValueError('Длина имени выделенного сервера не может превышать 255 символов.')
        if comment and len(comment) > 255:
            raise ValueError('Длина комментария не может превышать 255 символов.')
        data = {
            'plan_id': plan_id,
            'preset_id': preset_id,
            'name': name,
            'payment_period': payment_period,
        }
        if os_id:
            data['os_id'] = os_id
        if cp_id:
            data['cp_id'] = cp_id
        if bandwidth_id:
            data['bandwidth_id'] = bandwidth_id
        if network_drive_id:
            data['network_drive_id'] = network_drive_id
        if additional_ip_addr_id:
            data['additional_ip_addr_id'] = additional_ip_addr_id
        if comment:
            data['comment'] = comment
        prepared_json = json.dumps(data, cls=schemas.PaymentPeriodsEncoder)
        dedic = self._request(
            'POST', '/dedicated-servers', data=prepared_json,
            headers={'Content-Type': 'application/json'}
        )
        return schemas.DedicatedServerResponse(**dedic.json())

    def get(self, dedicated_id: int) -> schemas.DedicatedServerResponse:
        '''Получение информации о выделенном сервере.

        Args:
            dedicated_id (int): UID выделенного сервера.

        Returns:
            DedicatedServerResponse: Ответ от API.
        '''
        dedic = self._request(
            'GET', f'/dedicated-servers/{dedicated_id}'
        )
        return schemas.DedicatedServerResponse(**dedic.json())

    def update(
        self, dedicated_id: int, name: str | None = None,
        comment: str | None = None
    ) -> schemas.DedicatedServerResponse:
        '''Обновление выделенного сервера.

        Args:
            dedicated_id (int): UID выделенного сервера.
            name (str | None, optional): Имя выделенного сервера. Defaults to None.
            comment (str | None, optional): Комментарий. Defaults to None.

        Raises:
            ValueError: Если длина имени/комментария выделенного сервера больше 255 символов.

        Returns:
            DedicatedServerResponse: Ответ от API.
        '''
        if name and len(name) > 255:
            raise ValueError('Длина имени выделенного сервера не может превышать 255 символов.')
        if comment and len(comment) > 255:
            raise ValueError('Длина комментария не может превышать 255 символов.')
        data = {}
        if name:
            data['name'] = name
        if comment:
            data['comment'] = comment
        dedic = self._request(
            'PATCH', f'/dedicated-servers/{dedicated_id}', json=data
        )
        return schemas.DedicatedServerResponse(**dedic.json())

    def delete(self, dedicated_id: int) -> bool:
        '''Удаление выделенного сервера.

        Args:
            dedicated_id (int): UID выделенного сервера.

        Returns:
            bool: True, если сервер успешно удален.
        '''
        self._request(
            'DELETE', f'/dedicated-servers/{dedicated_id}'
        )
        return True

    def get_presets(self, location: str | None = None) -> schemas.DedicatedServerPresets:
        '''Получение списка тарифов выделенных серверов.

        Args:
            location (str | None, optional): Локация. Defaults to None.

        Returns:
            DedicatedServerPresets: Ответ от API.
        '''
        params = {}
        if location:
            params['location'] = location
        presets = self._request(
            'GET', '/presets/dedicated-servers', params=params
        )
        return schemas.DedicatedServerPresets(**presets.json())

    def get_services(self, preset_id: int) -> schemas.DedicatedServerServices:
        '''Получение списка услуг выделенного сервера.

        Args:
            preset_id (int): UID тарифа выделенного сервера.

        Returns:
            DedicatedServerServices: Ответ от API.
        '''
        services = self._request(
            'GET', f'/presets/dedicated-servers/{preset_id}/additional-services'
        )
        return schemas.DedicatedServerServices(**services.json())
