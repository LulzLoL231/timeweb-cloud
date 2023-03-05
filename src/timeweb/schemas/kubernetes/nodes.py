# -*- coding: utf-8 -*-
'''Модели для работы с нодами Kubernetes.'''
from datetime import datetime

from ..base import ResponseWithMeta, BaseResponse, BaseData


class Node(BaseData):
    '''Модель ноды'''
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
    '''Модель группы нод'''
    id: int
    name: str
    created_at: datetime
    preset_id: int
    node_count: int


class NodeGroupsResponse(ResponseWithMeta):
    '''Ответ со списком групп нод'''
    node_groups: list[NodeGroup]


class NodeGroupResponse(BaseResponse):
    '''Ответ с группой нод'''
    node_group: NodeGroup


class NodesResponse(ResponseWithMeta):
    '''Модель со списком нод'''
    nodes: list[Node]
