# -*- coding: utf-8 -*-
'''Модели для работы с Kubernetes.'''
from decimal import Decimal
from datetime import datetime

from ..base import ResponseWithMeta, BaseResponse, BaseData, BaseDelete


class Cluster(BaseData):
    '''Модель кластера Kubernetes.'''
    id: int
    name: str
    created_at: datetime
    status: str
    description: str
    ha: bool
    k8s_version: str
    network_driver: str
    ingress: bool
    preset_id: int
    cpu: int | None = None
    ram: int | None = None
    disk: int | None = None


class ClustersResponse(ResponseWithMeta):
    '''Ответ со списком кластеров'''
    clusters: list[Cluster]


class ClusterResponse(BaseResponse):
    '''Ответ с кластером'''
    cluster: Cluster


class ClusterDelete(BaseResponse):
    '''Ответ с хэшом для подтверждения удаления кластера'''
    cluster_delete: BaseDelete


class K8SVersionsResponse(ResponseWithMeta):
    '''Ответ со списком версий kubernetes'''
    k8s_versions: list[str]


class K8SNetworksResponse(ResponseWithMeta):
    '''Ответ со списком сетевых драйверов kubernetes'''
    network_drivers: list[str]


class K8SPreset(BaseData):
    '''Модель тарифа kubernetes'''
    id: int
    description: str
    description_short: str
    price: Decimal
    cpu: int
    ram: int
    disk: int
    network: int
    type: str | None = None


class K8SPresetsResponse(ResponseWithMeta):
    '''Ответ со списком тарифов для kubernetes.'''
    k8s_presets: list[K8SPreset]
