# -*- coding: utf-8 -*-
'''Модели для работы с ресурсами кластеров Kubernetes.'''
from ..base import BaseResponse, BaseData


class Resource(BaseData):
    '''Информация о ресурсе кластера.

    Attributes:
        requested (int): Запрошенное количество ресурса
        allocatable (int): Доступное количество
        capacity (int): Общее количество
        used (int): Используемое количество
    '''
    requested: int = 0
    allocatable: int = 0
    capacity: int = 0
    used: int = 0


class ClusterResources(BaseData):
    '''Ресурсы кластера.

    Attributes:
        nodes (int): Количество нод
        cores (Resource): Процессорный ресурс
        memory (Resource): Ресурс по памяти
        pods (Resource): Поды в кластере
    '''
    nodes: int = 0
    cores: Resource
    memory: Resource
    pods: Resource


class ClusterResourcesResponse(BaseResponse):
    '''Ответ с ресурсами кластера

    Attributes:
        resources (ClusterResources): Ресурсы кластера
    '''
    resources: ClusterResources
