# -*- coding: utf-8 -*-
'''Методы API для работы с балансировщиками.

Балансировщик позволяет распределять входящий трафик между несколькими серверами для повышения доступности и отказоустойчивости вашего сервиса.

Документация: https://timeweb.cloud/api-docs#tag/Balansirovshiki'''
import logging
from ipaddress import IPv4Address, IPv6Address

from httpx import Client

from .base import BaseClient
from ..schemas import balancers as schemas


class BalancersAPI(BaseClient):
    '''Клиент для работы с API балансировщиками Timeweb Cloud'''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    def get_balancers(self) -> schemas.BalancersResponse:
        '''Получить список балансировщиков.

        Returns:
            BalancersResponse: Список балансировщиков.
        '''
        balancers = self._request(
            'GET', '/balancers'
        )
        return schemas.BalancersResponse(**balancers.json())

    def create(
        self, name: str, algo: schemas.BalancerAlgorithm | str, is_sticky: bool,
        is_use_proxy: bool, is_ssl: bool, is_keepalive: bool, port: int,
        proto: schemas.Protocol | str, path: str, inter: int, timeout: int,
        fall: int, rise: int, preset_id: int
    ) -> schemas.BalancerResponse:
        '''Создать балансировщик.

        Args:
            name (str): Название балансировщика.
            algo (BalancerAlgorithm | str): Алгоритм переключений балансировщика.
            is_sticky (bool): Сохраняется ли сессия.
            is_use_proxy (bool): Выступает ли балансировщик в качестве прокси.
            is_ssl (bool): Требуется ли перенаправление на SSL.
            is_keepalive (bool): Выдает ли балансировщик сигнал о проверке жизнеспособности.
            port (int): Порт балансировщика.
            proto (Protocol | str): Протокол балансировщика.
            path (str): Адрес балансировщика.
            inter (int): Интервал проверки.
            timeout (int): Таймаут ответа балансировщика.
            fall (int): Порог количества ошибок.
            rise (int): Порог количества успешных проверок.
            preset_id (int): UID тарифа балансировщика.

        Returns:
            BalancerResponse: Балансировщик.
        '''
        data = {
            'name': name,
            'is_sticky': is_sticky,
            'is_use_proxy': is_use_proxy,
            'is_ssl': is_ssl,
            'is_keepalive': is_keepalive,
            'port': port,
            'path': path,
            'inter': inter,
            'timeout': timeout,
            'fall': fall,
            'rise': rise,
            'preset_id': preset_id
        }
        if isinstance(algo, schemas.BalancerAlgorithm):
            data['algo'] = algo.value
        else:
            data['algo'] = algo
        if isinstance(proto, schemas.Protocol):
            data['proto'] = proto.value
        else:
            data['proto'] = proto
        balancer = self._request(
            'POST', '/balancers', json=data
        )
        return schemas.BalancerResponse(**balancer.json())

    def get(self, balancer_id: int) -> schemas.BalancerResponse:
        '''Получить балансировщик.

        Args:
            balancer_id (int): UID балансировщика.

        Returns:
            BalancerResponse: Балансировщик.
        '''
        balancer = self._request(
            'GET', f'/balancers/{balancer_id}'
        )
        return schemas.BalancerResponse(**balancer.json())

    def update(
        self, balancer_id: int, name: str | None = None,
        algo: schemas.BalancerAlgorithm | str | None = None,
        is_sticky: bool | None = None, is_use_proxy: bool | None = None,
        is_ssl: bool | None = None, is_keepalive: bool | None = None,
        port: int | None = None, proto: schemas.Protocol | str | None = None,
        path: str | None = None, inter: int | None = None,
        timeout: int | None = None, fall: int | None = None,
        rise: int | None = None, preset_id: int | None = None
    ) -> schemas.BalancerResponse:
        '''Обновить балансировщик.

        Args:
            balancer_id (int): UID балансировщика.
            name (str | None, optional): Название балансировщика. Defaults to None.
            algo (BalancerAlgorithm | str | None, optional): Алгоритм переключений балансировщика. Defaults to None.
            is_sticky (bool | None, optional): Сохраняется ли сессия. Defaults to None.
            is_use_proxy (bool | None, optional): Выступает ли балансировщик в качестве прокси. Defaults to None.
            is_ssl (bool | None, optional): Требуется ли перенаправление на SSL. Defaults to None.
            is_keepalive (bool | None, optional): Выдает ли балансировщик сигнал о проверке жизнеспособности. Defaults to None.
            port (int | None, optional): Порт балансировщика. Defaults to None.
            proto (Protocol | str | None, optional): Протокол балансировщика. Defaults to None.
            path (str | None, optional): Адрес балансировщика. Defaults to None.
            inter (int | None, optional): Интервал проверки. Defaults to None.
            timeout (int | None, optional): Таймаут ответа балансировщика. Defaults to None.
            fall (int | None, optional): Порог количества ошибок. Defaults to None.
            rise (int | None, optional): Порог количества успешных проверок. Defaults to None.
            preset_id (int | None, optional): UID тарифа балансировщика. Defaults to None.

        Returns:
            BalancerResponse: Балансировщик.
        '''
        data: dict[str, str | int] = {}
        if name is not None:
            data['name'] = name
        if algo is not None:
            if isinstance(algo, schemas.BalancerAlgorithm):
                data['algo'] = algo.value
            else:
                data['algo'] = algo
        if is_sticky:
            data['is_sticky'] = is_sticky
        if is_use_proxy:
            data['is_use_proxy'] = is_use_proxy
        if is_ssl:
            data['is_ssl'] = is_ssl
        if is_keepalive:
            data['is_keepalive'] = is_keepalive
        if port is not None:
            data['port'] = port
        if proto is not None:
            if isinstance(proto, schemas.Protocol):
                data['proto'] = proto.value
            else:
                data['proto'] = proto
        if path is not None:
            data['path'] = path
        if inter is not None:
            data['inter'] = inter
        if timeout is not None:
            data['timeout'] = timeout
        if fall is not None:
            data['fall'] = fall
        if rise is not None:
            data['rise'] = rise
        if preset_id is not None:
            data['preset_id'] = preset_id
        balancer = self._request(
            'PATCH', f'/balancers/{balancer_id}', json=data
        )
        return schemas.BalancerResponse(**balancer.json())

    def delete(self, balancer_id: int) -> bool:
        '''Удалить балансировщик.

        Args:
            balancer_id (int): UID балансировщика.

        Returns:
            bool: Успешность удаления.
        '''
        self._request(
            'DELETE', f'/balancers/{balancer_id}'
        )
        return True

    def get_balancer_ips(self, balancer_id: int) -> schemas.BalancerIPsResponse:
        '''Получить IP балансировщика.

        Args:
            balancer_id (int): UID IP балансировщика.

        Returns:
            BalancerIPsResponse: IP адреса балансировщика.
        '''
        balancer_ips = self._request(
            'GET', f'/balancers/{balancer_id}/ips'
        )
        return schemas.BalancerIPsResponse(**balancer_ips.json())

    def add_balancer_ips(
        self, balancer_id: int, ips: list[str | IPv4Address | IPv6Address]
    ) -> bool:
        '''Добавить IP адреса балансировщика.

        Args:
            balancer_id (int): UID балансировщика.
            ips (list[str | IPv4Address | IPv6Address]): IP адреса.

        Returns:
            bool: IP адреса добавлены.
        '''
        resp = self._request(
            'POST', f'/balancers/{balancer_id}/ips', json={'ips': ips}
        )
        return resp.is_success

    def delete_balancer_ips(
        self, balancer_id: int, ips: list[str | IPv4Address | IPv6Address]
    ) -> bool:
        '''Удаление IP адресов балансировщика.

        Args:
            balancer_id (int): UID балансировщика.
            ips (list[str | IPv4Address | IPv6Address]): IP адреса.

        Returns:
            bool: IP адреса удалены.
        '''
        resp = self._request(
            'DELETE', f'/balancers/{balancer_id}/ips', json={'ips': ips}
        )
        return resp.is_success

    def get_balancer_rules(self, balancer_id: int) -> schemas.BalancerRulesResponse:
        '''Получить правила балансировщика.

        Args:
            balancer_id (int): UID балансировщика.

        Returns:
            BalancerRulesResponse: Правила балансировщика.
        '''
        balancer_rules = self._request(
            'GET', f'/balancers/{balancer_id}/rules'
        )
        return schemas.BalancerRulesResponse(**balancer_rules.json())

    def add_balancer_rule(
        self, balancer_id: int, balancer_proto: schemas.Protocol | str,
        balancer_port: int, server_proto: schemas.Protocol | str,
        server_port: int
    ) -> schemas.BalancerRuleResponse:
        '''Добавить правило балансировщика.

        Args:
            balancer_id (int): UID балансировщика.
            balancer_proto (Protocol | str): Протокол балансировщика.
            balancer_port (int): Порт балансировщика.
            server_proto (Protocol | str): Протокол сервера.
            server_port (int): Порт сервера.

        Returns:
            BalancerRuleResponse: Добавленное правило.
        '''
        data: dict[str, str | int] = {}
        if isinstance(balancer_proto, schemas.Protocol):
            data['balancer_proto'] = balancer_proto.value
        else:
            data['balancer_proto'] = balancer_proto
        data['balancer_port'] = balancer_port
        if isinstance(server_proto, schemas.Protocol):
            data['server_proto'] = server_proto.value
        else:
            data['server_proto'] = server_proto
        data['server_port'] = server_port
        balancer_rule = self._request(
            'POST', f'/balancers/{balancer_id}/rules', json=data
        )
        return schemas.BalancerRuleResponse(**balancer_rule.json())

    def update_balancer_rule(
        self, balancer_id: int, rule_id: int,
        balancer_proto: schemas.Protocol | str, balancer_port: int,
        server_proto: schemas.Protocol | str, server_port: int
    ) -> schemas.BalancerRuleResponse:
        '''Добавить правило балансировщика.

        Args:
            balancer_id (int): UID балансировщика.
            rule_id (int): UID правила.
            balancer_proto (Protocol | str): Протокол балансировщика.
            balancer_port (int): Порт балансировщика.
            server_proto (Protocol | str): Протокол сервера.
            server_port (int): Порт сервера.

        Returns:
            BalancerRuleResponse: Обнавлённое правило.
        '''
        data: dict[str, str | int] = {}
        if isinstance(balancer_proto, schemas.Protocol):
            data['balancer_proto'] = balancer_proto.value
        else:
            data['balancer_proto'] = balancer_proto
        data['balancer_port'] = balancer_port
        if isinstance(server_proto, schemas.Protocol):
            data['server_proto'] = server_proto.value
        else:
            data['server_proto'] = server_proto
        data['server_port'] = server_port
        balancer_rule = self._request(
            'PATCH', f'/balancers/{balancer_id}/rules/{rule_id}', json=data
        )
        return schemas.BalancerRuleResponse(**balancer_rule.json())

    def delete_balancer_rule(self, balancer_id: int, rule_id: int) -> bool:
        '''Удалить правило балансировщика.

        Args:
            balancer_id (int): UID балансировщика.
            rule_id (int): UID правила.

        Returns:
            bool: Правило удалено.
        '''
        resp = self._request(
            'DELETE', f'/balancers/{balancer_id}/rules/{rule_id}'
        )
        return resp.is_success

    def get_presets(self) -> schemas.BalancerPresetsResponse:
        '''Получить список тарифов балансировщиков.

        Returns:
            BalancerPresetsResponse: Список тарифов.
        '''
        balancer_presets = self._request('GET', '/presets/balancers')
        return schemas.BalancerPresetsResponse(**balancer_presets.json())
