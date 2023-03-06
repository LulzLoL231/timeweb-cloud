# -*- coding: utf-8 -*-
'''Методы API для работы с проектами.

Проекты позволяют организовать ваши ресурсы в группы, соответствующие вашему стилю работы.

Документация: https://timeweb.cloud/api-docs#tag/Proekty'''
import logging

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import projects as schemas
from ..schemas.servers.cloud import VDSArray
from ..schemas.balancers import BalancersResponse
from ..schemas.s3 import BucketArray
from ..schemas.kubernetes import ClustersResponse
from ..schemas.dbs import DBArray
from ..schemas.servers.dedics import DedicatedServers


class ProjectsAPI(BaseAsyncClient):
    '''Клиент для работы с API проектов'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_projects(self) -> schemas.ProjectsResponse:
        '''Получить список всех проектов.

        Returns:
            schemas.ProjectsResponse: Список всех проектов.
        '''
        projects = await self._request(
            'GET', '/projects'
        )
        return schemas.ProjectsResponse(**projects.json())

    async def create_project(
        self, name: str, description: str | None = None,
        avatar_id: str | None = None
    ) -> schemas.ProjectResponse:
        '''Создать проект.

        Args:
            name (str): Имя проекта.
            description (str | None, optional): Описание. Defaults to None.
            avatar_id (str | None, optional): UID аватара. Defaults to None.

        Raises:
            ValueError: если длина строки превышает 255.

        Returns:
            schemas.ProjectResponse: Созданный проект
        '''
        if len(name) > 255:
            raise ValueError('"name" не может превышать 255 символов!')
        if description and len(description) > 255:
            raise ValueError('"description" не может превышать 255 символов!')
        if avatar_id and len(avatar_id) > 255:
            raise ValueError('"avatar_id" не может превышать 255 символов!')
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        if avatar_id:
            data['avatar_id'] = avatar_id
        new = await self._request(
            'POST', '/projects', json=data
        )
        return schemas.ProjectResponse(**new.json())

    async def get_project(self, project_id: int) -> schemas.ProjectResponse:
        '''Получить проект.

        Args:
            project_id (int): UID проекта.

        Returns:
            schemas.ProjectResponse: Проект.
        '''
        proj = await self._request(
            'GET', f'/projects/{project_id}'
        )
        return schemas.ProjectResponse(**proj.json())

    async def delete_project(self, project_id: int) -> bool:
        '''Удалить проект.

        Args:
            project_id (int): UID проекта.

        Returns:
            bool: Проект удалён?
        '''
        status = await self._request(
            'DELETE', f'/projects/{project_id}'
        )
        return status.is_success

    async def change_project(
        self, project_id: int, name: str | None = None,
        description: str | None = None, avatar_id: str | None = None
    ) -> schemas.ProjectResponse:
        '''Изменить проект.

        Args:
            project_id (int): UID проекта.
            name (str | None, optional): Имя проекта. Defaults to None.
            description (str | None, optional): Описание. Defaults to None.
            avatar_id (str | None, optional): UID аватара. Defaults to None.

        Raises:
            ValueError: если длина строки превышает 255.

        Returns:
            schemas.ProjectResponse: Изменённый проект
        '''
        if name and len(name) > 255:
            raise ValueError('"name" не может превышать 255 символов!')
        if description and len(description) > 255:
            raise ValueError('"description" не может превышать 255 символов!')
        if avatar_id and len(avatar_id) > 255:
            raise ValueError('"avatar_id" не может превышать 255 символов!')
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        if avatar_id:
            data['avatar_id'] = avatar_id
        new = await self._request(
            'PATCH', f'/projects/{project_id}', json=data
        )
        return schemas.ProjectResponse(**new.json())

    async def get_project_balancers(self, project_id: int) -> BalancersResponse:
        '''Получить список балансировщиков проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            BalancersResponse: Список балансировщиков.
        '''
        array = await self._request(
            'GET', f'/projects/{project_id}/resources/balancers'
        )
        return BalancersResponse(**array.json())

    async def add_project_balancer(
        self, project_id: int, resource_id: int
    ) -> schemas.ResourceResponse:
        '''Добавить балансировщика в проект.

        Args:
            project_id (int): UID проекта.
            resource_id (int): UID балансировщика.

        Returns:
            schemas.ResourceResponse: Ресурс проекта.
        '''
        res = await self._request(
            'POST', f'/projects/{project_id}/resources/balancers',
            json={'resource_id': resource_id}
        )
        return schemas.ResourceResponse(**res.json())

    async def get_project_buckets(self, project_id: int) -> BucketArray:
        '''Получить список хранилищ проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            BucketArray: Список хранилищ.
        '''
        array = await self._request(
            'GET', f'/projects/{project_id}/resources/buckets'
        )
        return BucketArray(**array.json())

    async def add_project_bucket(
        self, project_id: int, resource_id: int
    ) -> schemas.ResourceResponse:
        '''Добавить хранилище в проект.

        Args:
            project_id (int): UID проекта.
            resource_id (int): UID хранилища.

        Returns:
            schemas.ResourceResponse: Ресурс проекта.
        '''
        res = await self._request(
            'POST', f'/projects/{project_id}/resources/buckets',
            json={'resource_id': resource_id}
        )
        return schemas.ResourceResponse(**res.json())

    async def get_project_clusters(self, project_id: int) -> ClustersResponse:
        '''Получить список кластеров проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            ClustersResponse: Список кластеров.
        '''
        array = await self._request(
            'GET', f'/projects/{project_id}/resources/clusters'
        )
        return ClustersResponse(**array.json())

    async def add_project_cluster(
        self, project_id: int, resource_id: int
    ) -> schemas.ResourceResponse:
        '''Добавить кластер в проект.

        Args:
            project_id (int): UID проекта.
            resource_id (int): UID кластера.

        Returns:
            schemas.ResourceResponse: Ресурс проекта.
        '''
        res = await self._request(
            'POST', f'/projects/{project_id}/resources/clusters',
            json={'resource_id': resource_id}
        )
        return schemas.ResourceResponse(**res.json())

    async def get_project_servers(self, project_id: int) -> VDSArray:
        '''Получить список облачных серверов проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            VDSArray: Список облачных серверов.
        '''
        array = await self._request(
            'GET', f'/projects/{project_id}/resources/servers'
        )
        return VDSArray(**array.json())

    async def add_project_server(
        self, project_id: int, resource_id: int
    ) -> schemas.ResourceResponse:
        '''Добавить облачный сервер в проект.

        Args:
            project_id (int): UID проекта.
            resource_id (int): UID облачного сервера.

        Returns:
            schemas.ResourceResponse: Ресурс проекта.
        '''
        res = await self._request(
            'POST', f'/projects/{project_id}/resources/servers',
            json={'resource_id': resource_id}
        )
        return schemas.ResourceResponse(**res.json())

    async def get_project_dbs(self, project_id: int) -> DBArray:
        '''Получить список баз данных проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            DBArray: Список баз данных.
        '''
        array = await self._request(
            'GET', f'/projects/{project_id}/resources/databases'
        )
        return DBArray(**array.json())

    async def add_project_db(
        self, project_id: int, resource_id: int
    ) -> schemas.ResourceResponse:
        '''Добавить базу данных в проект.

        Args:
            project_id (int): UID проекта.
            resource_id (int): UID базы данных.

        Returns:
            schemas.ResourceResponse: Ресурс проекта.
        '''
        res = await self._request(
            'POST', f'/projects/{project_id}/resources/databases',
            json={'resource_id': resource_id}
        )
        return schemas.ResourceResponse(**res.json())

    async def get_project_dedics(self, project_id: int) -> DedicatedServers:
        '''Получить список выделенных серверов проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            DedicatedServers: Список выделенных серверов.
        '''
        array = await self._request(
            'GET', f'/projects/{project_id}/resources/dedicated'
        )
        return DedicatedServers(**array.json())

    async def add_project_dedic(
        self, project_id: int, resource_id: int
    ) -> schemas.ResourceResponse:
        '''Добавить выделенный сервер в проект.

        Args:
            project_id (int): UID проекта.
            resource_id (int): UID выделенного сервера.

        Returns:
            schemas.ResourceResponse: Ресурс проекта.
        '''
        res = await self._request(
            'POST', f'/projects/{project_id}/resources/dedicated',
            json={'resource_id': resource_id}
        )
        return schemas.ResourceResponse(**res.json())

    async def get_project_resources(self, project_id: int) -> schemas.ResourcesResponse:
        '''Получить ресурсы проекта.

        Args:
            project_id (int): UID проекта.

        Returns:
            schemas.ResourcesResponse: Ресурсы проекта.
        '''
        res = await self._request(
            'GET', f'/projects/{project_id}/resources'
        )
        return schemas.ResourcesResponse(**res.json())

    async def get_account_balancers(self) -> BalancersResponse:
        '''Получить список балансировщиков аккаунта.

        Returns:
            BalancersResponse: Список балансировщиков.
        '''
        array = await self._request(
            'GET', '/projects/resources/balancers'
        )
        return BalancersResponse(**array.json())

    async def get_account_servers(self) -> VDSArray:
        '''Получить список облачных серверов аккаунта.

        Returns:
            VDSArray: Список облачных серверов.
        '''
        array = await self._request(
            'GET', '/projects/resources/servers'
        )
        return VDSArray(**array.json())

    async def get_account_buckets(self) -> BucketArray:
        '''Получить список хранилищ аккаунта.

        Returns:
            BucketArray: Список хранилищ.
        '''
        array = await self._request(
            'GET', '/projects/resources/buckets'
        )
        return BucketArray(**array.json())

    async def get_account_clusters(self) -> ClustersResponse:
        '''Получить список кластеров аккаунта.

        Returns:
            ClustersResponse: Список кластеров.
        '''
        array = await self._request(
            'GET', '/projects/resources/clusters'
        )
        return ClustersResponse(**array.json())

    async def get_account_dbs(self) -> DBArray:
        '''Получить список баз данных аккаунта.

        Returns:
            DBArray: Список баз данных.
        '''
        array = await self._request(
            'GET', '/projects/resources/databases'
        )
        return DBArray(**array.json())

    async def get_account_dedics(self) -> DedicatedServers:
        '''Получить список выделенных серверов аккаунта.

        Returns:
            DedicatedServers: Список выделенных серверов.
        '''
        array = await self._request(
            'GET', '/projects/resources/dedicated'
        )
        return DedicatedServers(**array.json())

    async def move_resource(
        self, project_id: int, to_project: int, resource_id: int,
        resource_type: str
    ) -> schemas.ResourceResponse:
        '''Перенести ресурс из одного проекта в другой.

        Args:
            project_id (int): UID проекта.
            to_project (int): UID проекта, куда переносится ресурс.
            resource_id (int): UID ресурса.
            resource_type (str): Тип ресурса.

        References:
            https://timeweb.cloud/api-docs#tag/Proekty/paths/~1api~1v1~1projects~1%7Bproject_id%7D~1resources~1transfer/put

        Returns:
            schemas.ResourceResponse: Изменённый ресурс.
        '''
        data = {
            'to_project': to_project,
            'resource_id': resource_id,
            'resource_type': resource_type
        }
        res = await self._request(
            'PUT', f'/projects/{project_id}/resources/transfer',
            json=data
        )
        return schemas.ResourceResponse(**res.json())
