# -*- coding: utf-8 -*-
'''Методы API для работы с API облачных серверов.

Облачные серверы — это способ размещения данных, при котором вы получаете полный доступ (root-доступ) к виртуальному серверу и его настройкам.
Вы можете гибко масштабировать параметры (процессор, память, диск) сервера, постепенно добавляя необходимые мощности,
когда растет нагрузка, и снижать их, когда нагрузка уменьшается.
Соответствующим образом будет увеличиваться или уменьшаться стоимость сервера.

Документация: https://timeweb.cloud/api-docs#tag/Oblachnye-servery'''
import json
import logging

from httpx import Client

from .base import BaseClient
from ..schemas.servers import cloud as schemas


class VDSAPI(BaseClient):
    '''Клиент для работы с API облачных серверов.'''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    def get_all(self, limit: int = 100, offset: int = 0) -> schemas.VDSArray:
        '''Возвращает список серверов.

        Args:
            limit (int, optional): Лимит выдачи. Defaults to 100.
            offset (int, optional): Смещение. Defaults to 0.

        Returns:
            schemas.VDSArray: Список облачных серверов.
        '''
        vds = self._request(
            'GET', '/servers'
        )
        vds.raise_for_status()
        return schemas.VDSArray(**vds.json())

    def get(self, server_id: int) -> schemas.VDSResponse:
        '''Возвращает сервер.

        Args:
            server_id (int): UID сервера.

        Returns:
            schemas.VDSResponse: Облачный сервер.
        '''
        vds = self._request(
            'GET', f'/servers/{server_id}'
        )
        return schemas.VDSResponse(**vds.json())

    def delete(self, server_id: int) -> bool:
        '''Удаление сервера.

        Args:
            server_id (int): UID сервера.

        Returns:
            bool: Сервер удалён?
        '''
        status = self._request(
            'DELETE', f'/servers/{server_id}'
        )
        return status.is_success

    def create(
        self, name: str, os_id: int, is_ddos_guard: bool,
        bandwidth: int, preset_id: int | None = None,
        configurator: dict[str, int] | None = None,
        software_id: int | None = None, avatar_id: str | None = None,
        comment: str | None = None, ssh_keys_ids: list[int] | None = None,
        is_local_network: bool | None = None
    ) -> schemas.VDSResponse:
        '''Создание облачного сервера.

        Args:
            name (str): Имя сервера.
            os_id (int): UID ОС сервера.
            is_ddos_guard (bool): Защита от DDOS.
            bandwidth (int): Пропускная способность.
            preset_id (int | None, optional): UID тарифа. Defaults to None.
            configurator (dict[str, int] | None, optional): Объект конфигуратора. Defaults to None.
            software_id (int | None, optional): UID ПО сервера. Defaults to None.
            avatar_id (str | None, optional): UID аватара сервера. Defaults to None.
            comment (str | None, optional): Комментарий к серверу. Defaults to None.
            ssh_keys_ids (list[int] | None, optional): Список UID SSH-ключей. Defaults to None.
            is_local_network (bool | None, optional): Локальная сеть. Defaults to None.

        Raises:
            ValueError: В случае неверного использования переменных.

        Returns:
            schemas.VDSResponse: Созданный облачный сервер.
        '''
        if not configurator and not preset_id:
            raise ValueError('Обязательно нужно указать configurator или preset_id!')
        if configurator and preset_id:
            raise ValueError('Нельзя указать одновременно configurator и preset_id!')
        if bandwidth not in range(100, 1100, 100):
            raise ValueError('Указаный bandwidth не подходит, только число от 100 до 1000 с шагом 100!')
        if len(name) > 255:
            raise ValueError('name не может превышать 255 символов!')
        if comment and len(comment) > 255:
            raise ValueError('comment не может превышать 255 символов!')
        if configurator:
            if (
                not configurator.get('configurator_id')
            ) or (
                not configurator.get('disk')
            ) or (
                not configurator.get('cpu')
            ) or (
                not configurator.get('ram')
            ):
                raise ValueError(
                    'В объекте configurator отсутствуют необходимые значения!'
                )
        server_param = {
            'name': name, 'os_id': os_id,
            'is_ddos_guard': is_ddos_guard, 'bandwidth': bandwidth
        }
        if preset_id:
            server_param['preset_id'] = preset_id
        if configurator:
            server_param['configurator'] = configurator
        if software_id:
            server_param['software_id'] = software_id
        if avatar_id:
            server_param['avatar_id'] = avatar_id
        if comment:
            server_param['comment'] = comment
        if ssh_keys_ids:
            server_param['ssh_keys_ids'] = ssh_keys_ids
        if is_local_network:
            server_param['is_local_network'] = is_local_network
        created_vds = self._request(
            'POST', '/servers', json=server_param
        )
        return schemas.VDSResponse(**created_vds.json())

    def update(
        self, server_id: int, name: str | None = None,
        os_id: int | None = None, bandwidth: int | None = None,
        preset_id: int | None = None, comment: str | None = None,
        configurator: dict[str, int] | None = None,
        software_id: int | None = None, avatar_id: str | None = None
    ) -> schemas.VDSResponse:
        '''Изменение сервера.

        Args:
            server_id (int): UID сервера.
            name (str | None, optional): Имя сервера. Defaults to None.
            os_id (int | None, optional): UID ОС сервера. Defaults to None.
            bandwidth (int | None, optional): Пропускная способность. Defaults to None.
            preset_id (int | None, optional): UID тарифа. Defaults to None.
            comment (str | None, optional): Комментарий к серверу. Defaults to None.
            configurator (dict[str, int] | None, optional): Объект конфигуратора. Defaults to None.
            software_id (int | None, optional): UID ПО. Defaults to None.
            avatar_id (str | None, optional): UID аватара сервера. Defaults to None.

        Returns:
            schemas.VDSResponse: Измененный сервер.
        '''
        if configurator and preset_id:
            raise ValueError(
                'Нельзя указать одновременно configurator и preset_id!')
        if bandwidth and bandwidth not in range(100, 1100, 100):
            raise ValueError(
                'Указаный bandwidth не подходит, только число от 100 до 1000 с шагом 100!')
        if name and len(name) > 255:
            raise ValueError('name не может превышать 255 символов!')
        if comment and len(comment) > 255:
            raise ValueError('comment не может превышать 255 символов!')
        if configurator:
            if (
                not configurator.get('configurator_id')
            ) or (
                not configurator.get('disk')
            ) or (
                not configurator.get('cpu')
            ) or (
                not configurator.get('ram')
            ):
                raise ValueError(
                    'В объекте configurator отсутствуют необходимые значения!'
                )
        server_param: dict[str, str | int | dict[str, int]] = {}
        if name:
            server_param['name'] = name
        if os_id:
            server_param['os_id'] = os_id
        if bandwidth:
            server_param['bandwidth'] = bandwidth
        if preset_id:
            server_param['preset_id'] = preset_id
        if configurator:
            server_param['configurator'] = configurator
        if software_id:
            server_param['software_id'] = software_id
        if avatar_id:
            server_param['avatar_id'] = avatar_id
        if comment:
            server_param['comment'] = comment
        updated_vds = self._request(
            'PATCH', f'/servers/{server_id}',
            json=server_param
        )
        return schemas.VDSResponse(**updated_vds.json())
