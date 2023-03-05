# -*- coding: utf-8 -*-
'''Методы API для работы с kubernetes.

Kubernetes — программное обеспечение с открытым исходным кодом, предназначенное для автоматизированного управления контейнерными приложениями

Документация: https://timeweb.cloud/api-docs#tag/Kubernetes'''
import logging
import warnings
from datetime import timedelta

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import kubernetes as schemas


class KubernetesAPI(BaseAsyncClient):
    '''Клиент для работы с API Kubernetes'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_clusters(
        self, limit: int = 100, offset: int = 0
    ) -> schemas.ClustersResponse:
        '''Получить список кластеров.

        Args:
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Сдвиг. Defaults to 0.

        Returns:
            schemas.ClustersResponse: Список кластеров.
        '''
        params = {
            'limit': limit,
            'offset': offset
        }
        clusters = await self._request(
            'GET', '/k8s/clusters', params=params
        )
        return schemas.ClustersResponse(**clusters.json())

    async def create(
        self, name: str, ha: bool, k8s_version: str,
        network_driver: str, ingress: bool, preset_id: int,
        worker_groups: list[dict[str, str | int]],
        description: str | None = None
    ) -> schemas.ClusterResponse:
        '''Создать кластер kuberneters.

        Args:
            name (str): Имя кластера.
            ha (bool): Описание появится позднее.
            k8s_version (str): Версия Kubernetes.
            network_driver (str): Сетевой драйвер кластера.
            ingress (bool): Использовать ingress в кластере?
            preset_id (int): UID тарифа мастер-ноды.
            worker_groups (list[dict[str, str  |  int]]): Группы воркеров в кластере.
            description (str | None, optional): Описание кластера. Defaults to None.

        Note:
            `worker_groups` это список со словарями с ключами `name`, `preset_id` и `node_count`.

        Raises:
            ValueError: если тип данных в `worker_groups` не верен.

        Returns:
            schemas.ClusterResponse: Созданный кластер.
        '''
        data: dict[str, str | int | list[dict[str, str | int]]] = {
            'name': name,
            'ha': ha,
            'k8s_version': k8s_version,
            'network_driver': network_driver,
            'ingress': ingress,
            'preset_id': preset_id
        }
        if description:
            data['description'] = description
        # TODO: Мне чёт не нравится как сделана валидация,
        # с другой стороны, этот кусок нужен только тут.
        if not isinstance(worker_groups, list):
            raise ValueError('"worker_groups" должен быть списком!')
        else:
            if len(worker_groups) == 0:
                raise ValueError('"worker_groups" не должен быть пустым списком!')
            else:
                for idx, grp in enumerate(worker_groups):
                    if not isinstance(grp, dict):
                        raise ValueError(f'Объект #{idx} в "worker_groups" не словарь!')
                    else:
                        if 'name' not in grp:
                            raise ValueError(
                                f'В словаре #{idx} в "worker_groups" нету "name"!'
                            )
                        else:
                            if not isinstance(grp['name'], str):
                                raise ValueError(
                                    f'В словаре #{idx} в "worker_groups" - "name" не str!'
                                )
                        if 'preset_id' not in grp:
                            raise ValueError(
                                f'В словаре #{idx} в "worker_groups" нету "preset_id"!'
                            )
                        else:
                            if not isinstance(grp['preset_id'], int):
                                raise ValueError(
                                    f'В словаре #{idx} в "worker_groups" - "preset_id" не int!'
                                )
                        if 'node_count' not in grp:
                            raise ValueError(
                                f'В словаре #{idx} в "worker_groups" нету "node_count"!'
                            )
                        else:
                            if not isinstance(grp['node_count'], int):
                                raise ValueError(
                                    f'В словаре #{idx} в "worker_groups" - "node_count" не int!'
                                )
        data['worker_groups'] = worker_groups
        new_cluster = await self._request(
            'POST', '/k8s/clusters'
        )
        return schemas.ClusterResponse(**new_cluster.json())

    async def get_cluster(self, cluster_id: int) -> schemas.ClusterResponse:
        '''Получить информацию о кластере.

        Args:
            cluster_id (int): UID кластера.

        Returns:
            schemas.ClusterResponse: Информация о кластере.
        '''
        cluster = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}'
        )
        return schemas.ClusterResponse(**cluster.json())

    async def cluster_delete(self, cluster_id: int) -> schemas.ClusterDelete | bool:
        '''Удалить кластер.

        Args:
            cluster_id (int): UID кластера.

        Note:
            Вернёт `schemas.ClusterDelete`, если активно подтверждение удаления сервисов.

        Returns:
            schemas.ClusterDelete | bool: Хэш для удаления, или кластер удалён?
        '''
        delete = await self._request(
            'DELETE', f'/k8s/clusters/{cluster_id}'
        )
        if delete.status_code == 204:
            return True
        elif delete.status_code == 200:
            return schemas.ClusterDelete(**delete.json())
        else:
            return False

    async def confirm_cluster_delete(
        self, cluster_id: int, hash: str, code: int
    ) -> bool:
        '''Подтвердить удаление кластера.

        Args:
            cluster_id (int): UID кластера.
            hash (str): Хэш для удаления. Из `self.request_cluster_delete`.
            code (int): Код для подтверждения удаления.

        Returns:
            bool: Кластер удалён?
        '''
        params = {
            'hash': hash,
            'code': code
        }
        status = await self._request(
            'DELETE', f'/k8s/clusters/{cluster_id}',
            params=params
        )
        if status.status_code == 204 and status.elapsed > timedelta(seconds=2):
            return True
        else:
            if status.status_code == 204:
                warnings.warn(
                    'API слишком быстро подтвердил удаление. '
                    'Возможно он врёт. Проверьте хэш!'
                )
                return True
            return False

    async def update_cluster(self, cluster_id: int, description: str) -> schemas.ClusterResponse:
        '''Обновить информацию о кластере.

        Args:
            cluster_id (int): UID кластера.
            description (str): Новое описание кластера.

        Returns:
            schemas.ClusterResponse: Обновлённый кластер.
        '''
        updated = await self._request(
            'PATCH', f'/k8s/clusters/{cluster_id}',
            json={'description': description}
        )
        return schemas.ClusterResponse(**updated.json())

    async def get_cluster_resources(
        self, cluster_id: int
    ) -> schemas.ClusterResourcesResponse:
        '''Получить ресурсы кластера.

        Args:
            cluster_id (int): UID кластера.

        Returns:
            schemas.ClusterResourcesResponse: Информация о ресурсах кластера.
        '''
        info = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}/resources'
        )
        return schemas.ClusterResourcesResponse(**info.json())

    async def get_cluster_kubeconfig(self, cluster_id: int) -> str:
        '''Получить файл kubeconfig кластера.

        Args:
            cluster_id (int): UID кластера.

        Returns:
            str: YAML файл kubeconfig.
        '''
        kc = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}/kubeconfig'
        )
        return kc.text

    async def get_cluster_groups(self, cluster_id: int) -> schemas.NodeGroupsResponse:
        '''Получить группы нод кластера.

        Args:
            cluster_id (int): UID кластера.

        Returns:
            schemas.NodeGroupsResponse: Список групп нод.
        '''
        groups = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}/groups'
        )
        return schemas.NodeGroupsResponse(**groups.json())

    async def create_cluster_group(
        self, cluster_id: int, name: str, preset_id: int, node_count: int
    ) -> schemas.NodeGroupResponse:
        '''Создать группу нод кластера.

        Args:
            cluster_id (int): UID кластера.
            name (str): Имя группы.
            preset_id (int): UID тарифа воркер-ноды.
            node_count (int): Кол-во нод в группе.

        Raises:
            ValueError: если "node_count" меньше 1-ого.

        Returns:
            schemas.NodeGroupResponse: Информация о группе нод.
        '''
        if node_count < 1:
            raise ValueError('"node_count" должен быть больше 1-ого.')
        data = {
            'name': name,
            'preset_id': preset_id,
            'node_count': node_count
        }
        group = await self._request(
            'POST', f'/k8s/clusters/{cluster_id}/groups',
            json=data
        )
        return schemas.NodeGroupResponse(**group.json())

    async def get_cluster_group(
        self, cluster_id: int, group_id: int
    ) -> schemas.NodeGroupResponse:
        '''Получить информацию о группе нод.

        Args:
            cluster_id (int): UID кластера.
            group_id (int): UID группы нод.

        Returns:
            schemas.NodeGroupResponse: Информация о группе нод.
        '''
        group = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}/groups/{group_id}'
        )
        return schemas.NodeGroupResponse(**group.json())

    async def delete_cluster_group(self, cluster_id: int, group_id: int) -> bool:
        '''Удалить группу нод кластера.

        Args:
            cluster_id (int): UID кластера.
            group_id (int): UID группы нод.

        Returns:
            bool: Группа нод удалена?
        '''
        status = await self._request(
            'DELETE', f'/k8s/clusters/{cluster_id}/groups/{group_id}'
        )
        return status.is_success

    async def get_cluster_group_nodes(
        self, cluster_id: int, group_id: int, limit: int = 100,
        offset: int = 0
    ) -> schemas.NodesResponse:
        '''Получить список нод принадлежащих группе.

        Args:
            cluster_id (int): UID кластера.
            group_id (int): UID группы нод.
            limit (int, optional): Сколько записей вернуть. Defaults to 100.
            offset (int, optional): Сдвиг. Defaults to 0.

        Returns:
            schemas.NodesResponse: Список нод.
        '''
        params = {
            'limit': limit,
            'offset': offset
        }
        nodes = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}/groups/{group_id}/nodes',
            params=params
        )
        return schemas.NodesResponse(**nodes.json())

    async def increase_cluster_group_nodes(
        self, cluster_id: int, group_id: int, count: int
    ) -> schemas.NodesResponse:
        '''Увеличить кол-во нод в группе на указанное значение.

        Args:
            cluster_id (int): UID кластера.
            group_id (int): UID группы нод.
            count (int): Количество нод. Больше 1-ого.

        Raises:
            ValueError: если `count` меньше 1-ого.

        Returns:
            schemas.NodesResponse: Список нод.
        '''
        if count < 1:
            raise ValueError('"count" не может быть меньше 1-ого!')
        nodes = await self._request(
            'POST', f'/k8s/clusters/{cluster_id}/groups/{group_id}/nodes',
            json={'count': count}
        )
        return schemas.NodesResponse(**nodes.json())

    async def decrease_cluster_group_nodes(
        self, cluster_id: int, group_id: int, count: int
    ) -> bool:
        '''Уменьшить кол-во нод в группе на указанное значение.

        Args:
            cluster_id (int): UID кластера.
            group_id (int): UID группы нод.
            count (int): Количество нод. Больше 1-ого.

        Raises:
            ValueError: если `count` меньше 1-ого.

        Returns:
            bool: Кол-во нод уменьшено?
        '''
        if count < 1:
            raise ValueError('"count" не может быть меньше 1-ого!')
        status = await self._request(
            'DELETE', f'/k8s/clusters/{cluster_id}/groups/{group_id}/nodes',
            json={'count': count}
        )
        return status.is_success

    async def get_cluster_nodes(self, cluster_id: int) -> schemas.NodesResponse:
        '''Получить список нод кластера.

        Args:
            cluster_id (int): UID кластера.

        Returns:
            schemas.NodesResponse: Список нод.
        '''
        nodes = await self._request(
            'GET', f'/k8s/clusters/{cluster_id}/nodes'
        )
        return schemas.NodesResponse(**nodes.json())

    async def delete_cluster_node(self, cluster_id: int, node_id: int) -> bool:
        '''Удалить ноду кластера.

        Args:
            cluster_id (int): UID кластера.
            node_id (int): UID ноды.

        Returns:
            bool: Нода удалена?
        '''
        status = await self._request(
            'DELETE', f'/k8s/clusters/{cluster_id}/nodes/{node_id}'
        )
        return status.is_success

    async def get_k8s_versions(self) -> schemas.K8SVersionsResponse:
        '''Получить список версий Kubernetes.

        Returns:
            schemas.K8SVersionsResponse: Список версий Kubernetes.
        '''
        info = await self._request(
            'GET', '/k8s/k8s_versions'
        )
        return schemas.K8SVersionsResponse(**info.json())

    async def get_k8s_network_drivers(self) -> schemas.K8SNetworksResponse:
        '''Получить список сетевых драйверов kubernetes.

        Returns:
            schemas.K8SNetworksResponse: Список сетевых драйверов.
        '''
        info = await self._request(
            'GET', '/k8s/network_drivers'
        )
        return schemas.K8SNetworksResponse(**info.json())

    async def get_k8s_presets(self) -> schemas.K8SPresetsResponse:
        '''Получить список тарифов kubernetes.

        Returns:
            schemas.K8SPresetsResponse: Список тарифов.
        '''
        info = await self._request(
            'GET', '/presets/k8s'
        )
        return schemas.K8SPresetsResponse(**info.json())
