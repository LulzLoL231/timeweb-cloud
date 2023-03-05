# -*- coding: utf-8 -*-
'''Модели для работы с ресурсами кластеров Kubernetes.'''
from ..base import BaseResponse, BaseData


class Resource(BaseData):
    '''Информация о ресурсе кластера'''
    requested: int = 0
    allocatable: int = 0
    capacity: int = 0
    used: int = 0


class ClusterResources(BaseData):
    '''Ресурсы кластера'''
    nodes: int = 0
    cores: Resource
    memory: Resource
    pods: Resource


class ClusterResourcesResponse(BaseResponse):
    '''Ответ с ресурсами кластера'''
    resources: ClusterResources
