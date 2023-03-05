# -*- coding: utf-8 -*-
'''Методы API для работы с API облачных серверов.

Облачные серверы — это способ размещения данных, при котором вы получаете полный доступ (root-доступ) к виртуальному серверу и его настройкам.
Вы можете гибко масштабировать параметры (процессор, память, диск) сервера, постепенно добавляя необходимые мощности,
когда растет нагрузка, и снижать их, когда нагрузка уменьшается.
Соответствующим образом будет увеличиваться или уменьшаться стоимость сервера.

Документация: https://timeweb.cloud/api-docs#tag/Oblachnye-servery'''
import logging
from datetime import datetime, date
from ipaddress import IPv4Address, IPv6Address

from httpx import Client

from .base import BaseClient
from ..schemas.servers import cloud as schemas


IPAddress = IPv4Address | IPv6Address


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
        self, name: str, is_ddos_guard: bool, bandwidth: int,
        os_id: int | None = None, preset_id: int | None = None,
        configurator: dict[str, int] | None = None, image_id: int | None = None,
        software_id: int | None = None, avatar_id: str | None = None,
        comment: str | None = None, ssh_keys_ids: list[int] | None = None,
        is_local_network: bool | None = None
    ) -> schemas.VDSResponse:
        '''Создание облачного сервера.

        Args:
            name (str): Имя сервера.
            is_ddos_guard (bool): Защита от DDOS.
            bandwidth (int): Пропускная способность.
            os_id (int | None, optional): UID ОС сервера. Defaults to None.
            image_id (int | None, optional): UID образа. Defaults to None.
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
        if os_id and image_id:
            raise ValueError('Нельзя одновременно использовать "os_id" и "image_id"!')
        server_param = {
            'name': name,
            'is_ddos_guard': is_ddos_guard, 'bandwidth': bandwidth
        }
        if os_id:
            server_param['os_id'] = os_id
        if image_id:
            server_param['image_id'] = image_id
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

    def make_action(self, server_id: int, action: str) -> bool:
        '''Выполнить действие над сервером.

        Args:
            server_id (int): UID сервера.
            action (str): Имя действия.

        Note:
            `action` можно найти тут https://timeweb.cloud/api-docs#tag/Oblachnye-servery/paths/~1api~1v1~1servers~1%7Bserver_id%7D~1action/post

        Returns:
            bool: Успешное выполнение действия.
        '''
        status = self._request(
            'POST', f'/servers/{server_id}/action',
            json={'action': action}
        )
        return status.is_success

    def clone(self, server_id: int) -> dict:
        '''Клонировать сервер.

        Args:
            server_id (int): UID сервера.

        Returns:
            dict: Объект сервера.
        '''
        server = self._request(
            'POST', f'/servers/{server_id}/clone'
        )
        return server.json()

    def get_statistics(self, server_id: int, date_from: datetime | str, date_to: datetime | str) -> dict:
        '''Получить статистику сервера.

        Args:
            server_id (int): UID сервера.
            date_from (datetime | str): Дата начала сбора статистика.
            date_to (datetime | str): Дата конца сбора статистики.

        Returns:
            dict: Объект статистики сервера.
        '''
        params = {
            'date_from': date_from,
            'date_to': date_to
        }
        if isinstance(date_from, datetime):
            params['date_from'] = date_from.isoformat()
        if isinstance(date_to, datetime):
            params['date_to'] = date_to.isoformat()
        stats = self._request(
            'GET', f'/servers/{server_id}/statistics'
        )
        return stats.json()

    def get_os_list(self) -> dict:
        '''Получить список всех операционных систем.

        Returns:
            dict: Объект со списком ОС.
        '''
        os_array = self._request(
            'GET', '/os/servers'
        )
        return os_array.json()

    def get_presets(self) -> dict:
        '''Получить список всех тарифов.

        Returns:
            dict: Объект со списком тарифов.
        '''
        presets = self._request(
            'GET', '/presets/servers'
        )
        return presets.json()

    def get_configurators(self) -> dict:
        '''Получить список всеъ конфигураторов серверов.

        Returns:
            dict: Объект со списком конфигураторов.
        '''
        confs = self._request(
            'GET', '/configurator/servers'
        )
        return confs.json()

    def get_softwares(self) -> dict:
        '''Получить список ПО из маркетплейса.

        Returns:
            dict: Объект со списком ПО из маркетплейса.
        '''
        softwares = self._request(
            'GET', '/software/servers'
        )
        return softwares.json()

    def set_boot_mode(self, server_id: int, boot_mode: str) -> bool:
        '''Установка типа загрузки ОС сервера.
        После смены типа загрузки, сервер будет перезапущен.

        Args:
            server_id (int): UID сервера.
            boot_mode (str): Тип загрузки ОС.

        Note:
            `boot_mode` можно найти тут https://timeweb.cloud/api-docs#tag/Oblachnye-servery/paths/~1api~1v1~1servers~1%7Bserver_id%7D~1boot-mode/post

        Returns:
            bool: Тип загрузки изменён?
        '''
        status = self._request(
            'POST', f'/servers/{server_id}/boot-mode',
            json={'boot_mode': boot_mode}
        )
        return status.is_success

    def set_nat_mode(self, server_id: int, nat_mode: str) -> bool:
        '''Установка правила маршрутизации трафика сервера.

        Args:
            server_id (int): UID сервера.
            nat_mode (str): Правило для маршрутизации трафика.

        Note:
            `nat_mode` можно найти тут https://timeweb.cloud/api-docs#tag/Oblachnye-servery/paths/~1api~1v1~1servers~1%7Bserver_id%7D~1local-networks~1nat-mode/patch

        Returns:
            bool: Правила маршрутизации изменены?
        '''
        status = self._request(
            'POST', f'/servers/{server_id}/local-networks/nat-mode',
            json={'nat_mode': nat_mode}
        )
        return status.is_success

    def get_server_ips(self, server_id: int) -> dict:
        '''Получить список IP-адресов сервера.

        Args:
            server_id (int): UID сервера.

        Returns:
            dict: Объект со спиком IP-адресов сервера.
        '''
        ips = self._request(
            'GET', f'/servers/{server_id}/ips'
        )
        return ips.json()

    def add_server_ip(self, server_id: int, type: str, ptr: str) -> dict:
        '''Добавление IP-адреса сервера.

        Args:
            server_id (int): UID сервера.
            type (str): Тип IP-адреса.
            ptr (str): PTR запись IP-адреса.

        Returns:
            dict: Объект с новым IP-адресом сервера.
        '''
        new_ip = self._request(
            'POST', f'/servers/{server_id}/ips',
            json={'type': type, 'ptr': ptr}
        )
        return new_ip.json()

    def delete_server_ip(self, server_id: int, ip: IPAddress | str) -> bool:
        '''Удаление IP-адреса сервера.

        Args:
            server_id (int): UID сервера.
            ip (IPAddress | str): IP-адрес.

        Returns:
            bool: IP-адрес удалён?
        '''
        status = self._request(
            'DELETE', f'/servers/{server_id}/ips',
            json={'ip': str(ip)}
        )
        return status.is_success

    def update_server_ip(self, server_id: int, ip: IPAddress | str, ptr: str) -> dict:
        '''Добавление IP-адреса сервера.

        Args:
            server_id (int): UID сервера.
            ip (IPAddress | str): IP-адрес.
            ptr (str): PTR запись IP-адреса.

        Returns:
            dict: Объект с новым IP-адресом сервера.
        '''
        updated_ip = self._request(
            'PATCH', f'/servers/{server_id}/ips',
            json={'ip': ip, 'ptr': ptr}
        )
        return updated_ip.json()

    def get_logs(self, server_id: int, limit: int = 100, offset: int = 0, order: str = 'asc') -> dict:
        '''Получить логи сервера.

        Args:
            server_id (int): UID сервера.
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Смещение. Defaults to 0.
            order (str, optional): Сортировка по дате. Defaults to 'asc'.

        Returns:
            dict: Объект со списком логов.
        '''
        params = {
            'limit': limit,
            'offset': offset,
            'order': order
        }
        logs = self._request(
            'GET', f'/servers/{server_id}/logs',
            params=params
        )
        return logs.json()

    def get_server_disks(self, server_id: int) -> dict:
        '''Получить список дисков сервера.

        Args:
            server_id (int): UID сервера.

        Returns:
            dict: Объект со списком дисков сервера.
        '''
        disks = self._request(
            'GET', f'/servers/{server_id}/disks'
        )
        return disks.json()

    def create_server_disk(self, server_id: int, size: int) -> dict:
        '''Создать диск сервера.

        Args:
            server_id (int): UID сервера.
            size (int): Размер диска. Минимальный 5120, максимальный 512000, шаг 5120.

        Returns:
            dict: Созданный диск сервера.
        '''
        if size not in range(5120, 512001, 5120):
            raise ValueError('"size" вне допустимых пределах!')
        disk = self._request(
            'POST', f'/servers/{server_id}/disks',
            json={'size': size}
        )
        return disk.json()

    def get_server_disk(self, server_id: int, disk_id: int) -> dict:
        '''Получить диск сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.

        Returns:
            dict: Объект диска сервера.
        '''
        disk = self._request(
            'GET', f'/servers/{server_id}/disks/{disk_id}'
        )
        return disk.json()

    def update_server_disk(self, server_id: int, disk_id: int, size: int) -> dict:
        '''Изменить параметры диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            size (int): Размер диска. Минимальный 5120, максимальный 512000, шаг 5120.

        Returns:
            dict: Объект с обновленным диском сервера.
        '''
        if size not in range(5120, 512001, 5120):
            raise ValueError('"size" вне допустимых пределах!')
        disk = self._request(
            'PATCH', f'/servers/{server_id}/disks/{disk_id}',
            json={'size': size}
        )
        return disk.json()

    def delete_server_disk(self, server_id: int, disk_id: int) -> bool:
        '''Удалить сервер диска.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.

        Returns:
            bool: Диск сервера удалён?
        '''
        status = self._request(
            'DELETE', f'/servers/{server_id}/disks/{disk_id}'
        )
        return status.is_success

    def get_autobackup_settings(self, server_id: int, disk_id: int) -> dict:
        '''Получить настройка автобэкапов диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.

        Returns:
            dict: Объект настроек автобэкапа.
        '''
        settings = self._request(
            'GET', f'/servers/{server_id}/disks/{disk_id}/auto-backups'
        )
        return settings.json()

    def change_autobackup_settings(
        self, server_id: int, disk_id: int, is_enabled: bool,
        interval: str | None = None, creation_start_at: date | str | None = None,
        copy_count: int | None = None, day_of_week: int | None = None
    ) -> dict:
        '''Изменение настроек автобэкапа диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            is_enabled (bool): Автобэкап включён?
            interval (str | None, optional): Периодичность создания бэкапов. Defaults to None.
            creation_start_at (date | str | None, optional): Дата начала создания бэкапов. Defaults to None.
            copy_count (int | None, optional): Кол-во копий для хранения. Defaults to None.
            day_of_week (int | None, optional): День недели для бэкапа. Defaults to None.

        Note:
            При значении `is_enabled`: True, поля `copy_count`, `creation_start_at`, `interval` и  являются обязательными.

            `copy_count` чисто в интервале 1-99.

            `day_of_week` работает только со значением `interval`: week. Интервал 1-7.

        Returns:
            dict: Объект настроек автобекапов.
        '''
        data: dict[str, bool | str | int] = {
            'is_enabled': is_enabled
        }
        if is_enabled:
            if not copy_count:
                raise ValueError('Укажите "copy_count"!')
            if not interval:
                raise ValueError('Укажите "interval"!')
            else:
                data['interval'] = interval
            if not creation_start_at:
                raise ValueError('Укажите "creation_start_at"!')
            else:
                if isinstance(creation_start_at, date):
                    data['creation_start_at'] = creation_start_at.isoformat()
                else:
                    data['creation_start_at'] = creation_start_at
            if copy_count not in range(1, 100):
                raise ValueError('"copy_count" должен быть числом в интервале 1-99!')
            else:
                data['copy_count'] = copy_count
            if interval == 'week':
                if not day_of_week:
                    raise ValueError('При значении "interval": "week", "day_of_week" обязателен!')
                else:
                    if day_of_week not in range(1, 8):
                        raise ValueError('"day_of_week" число в интервале 1-7!')
                    else:
                        data['day_of_week'] = day_of_week
        settings = self._request(
            'PATCH', f'/servers/{server_id}/disks/{disk_id}/auto-backups',
            json=data
        )
        return settings.json()

    def make_server_disk_backup(
        self, server_id: int, disk_id: int, comment: str | None = None
    ) -> dict:
        '''Создание бэкапа диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            comment (str | None, optional): Комментарий к бэкапу. Defaults to None.

        Returns:
            dict: Объект бэкапа.
        '''
        backup = self._request(
            'POST', f'/servers/{server_id}/disks/{disk_id}/backups',
            json={'comment': comment} if comment else {}
        )
        return backup.json()

    def get_server_disk_backups(self, server_id: int, disk_id: int) -> dict:
        '''Получить список бэкапов диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.

        Returns:
            dict: Объект со списком бэкапов диска.
        '''
        backups = self._request(
            'GET', f'/servers/{server_id}/disks/{disk_id}/backups'
        )
        return backups.json()

    def change_server_disk_backup(
        self, server_id: int, disk_id: int, backup_id: int, comment: str
    ) -> dict:
        '''Изменение бэкапа диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            backup_id (int): UID бэкапа диска.
            comment (str): Комментарий.

        Returns:
            dict: Объект бэкапа диска.
        '''
        backup = self._request(
            'PATCH', f'/servers/{server_id}/disks/{disk_id}/backups/{backup_id}',
            json={'comment': comment}
        )
        return backup.json()

    def delete_server_disk_backup(
        self, server_id: int, disk_id: int, backup_id: int
    ) -> bool:
        '''Удаление бэкапа диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            backup_id (int): UID бэкапа.

        Returns:
            bool: Бэкап удалён?
        '''
        status = self._request(
            'DELETE', f'/servers/{server_id}/disks/{disk_id}/backups/{backup_id}'
        )
        return status.is_success

    def get_server_disk_backup(
        self, server_id: int, disk_id: int, backup_id: int
    ) -> dict:
        '''Получить бэкап диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            backup_id (int): UID бэкапа.

        Returns:
            dict: Объект бэкапа диска.
        '''
        backup = self._request(
            'GET', f'/servers/{server_id}/disks/{disk_id}/backups/{backup_id}'
        )
        return backup.json()

    def make_server_disk_backup_action(
        self, server_id: int, disk_id: int, backup_id: int, action: str
    ) -> bool:
        '''Выполнить действие над бэкапом диска сервера.

        Args:
            server_id (int): UID сервера.
            disk_id (int): UID диска сервера.
            backup_id (int): UID бэкапа.
            action (str): Действие над бэкапом.

        Note:
            `action` можно найти тут https://timeweb.cloud/api-docs#tag/Oblachnye-servery/paths/~1api~1v1~1servers~1%7Bserver_id%7D~1disks~1%7Bdisk_id%7D~1backups~1%7Bbackup_id%7D~1action/post

        Returns:
            dict: Объект бэкапа диска.
        '''
        backup = self._request(
            'POST', f'/servers/{server_id}/disks/{disk_id}/backups/{backup_id}',
            json={'action': action}
        )
        return backup.json()
