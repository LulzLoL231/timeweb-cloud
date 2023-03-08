# -*- coding: utf-8 -*-
'''Модели для работы с нодами Kubernetes.'''
from datetime import datetime

from ..base import ResponseWithMeta, BaseResponse, BaseData


class Node(BaseData):
    '''Модель ноды.

    Attributes:
        id (int): Уникальный идентификатор ноды
        created_at (datetime): Дата и время создания ноды в формате ISO8601
        type (str): Тип ноды
        group_id (int): Идентификатор группы нод
        status (str): Статус
        preset_id (int): Идентификатор тарифа ноды
        cpu (int): Количество ядер
        ram (int): Количество памяти
        disk (int): Количество пространства
        network (int): Пропускная способность сети
    '''
    id: int
    created_at: datetime
    type: str
    group_id: int
    status: str
    preset_id: int
    cpu: int
    ram: int
    disk: int
    network: int


class NodeGroup(BaseData):
    '''Модель группы нод

    Attributes:
        id (int): Уникальный идентификатор группы
        name (str): Название группы
        created_at (datetime): Дата и время создания группы в формате ISO8601
        preset_id (int): Идентификатор тарифа мастер-ноды
        node_count (int): Количество нод в группе
    '''
    id: int
    name: str
    created_at: datetime
    preset_id: int
    node_count: int


class NodeGroupsResponse(ResponseWithMeta):
    '''Ответ со списком групп нод

    Attributes:
        node_groups (list[NodeGroup]): Список групп нод
    '''
    node_groups: list[NodeGroup]


class NodeGroupResponse(BaseResponse):
    '''Ответ с группой нод

    Attributes:
        node_group (NodeGroup): Группа нод
    '''
    node_group: NodeGroup


class NodesResponse(ResponseWithMeta):
    '''Модель со списком нод

    Attributes:
        nodes (list[Node]): Список нод
    '''
    nodes: list[Node]
