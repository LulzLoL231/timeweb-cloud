# -*- coding: utf-8 -*-
'''Модели для работы с Kubernetes.'''
from decimal import Decimal
from datetime import datetime

from ..base import ResponseWithMeta, BaseResponse, BaseData, BaseDelete


class Cluster(BaseData):
    '''Модель кластера Kubernetes.

    Attributes:
        id (int): Уникальный идентификатор кластера
        name (str): Название
        created_at (datetime): Дата и время создания кластера в формате ISO8601
        status (str): Статус
        description (str): Описание
        ha (bool): Описание появится позже
        k8s_version (str): Версия Kubernetes
        network_driver (str): Используемый сетевой драйвер
        ingress (bool): Логическое значение, показывающее, включен ли Ingress
        preset_id (int): Идентификатор тарифа мастер-ноды
        cpu (int | None): Общее количество ядер
        ram (int | None): Общее количество памяти
        disk (int | None): Общее дисковое пространство
    '''
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
    '''Ответ со списком кластеров

    Attributes:
        clusters (list[Cluster]): Список кластеров
    '''
    clusters: list[Cluster]


class ClusterResponse(BaseResponse):
    '''Ответ с кластером

    Attributes:
        cluster (Cluster): Кластер
    '''
    cluster: Cluster


class ClusterDelete(BaseResponse):
    '''Ответ с хэшом для подтверждения удаления кластера

    Attributes:
        cluster_delete (BaseDelete): Оюъект с хэшом подтверждения удаления.
    '''
    cluster_delete: BaseDelete


class K8SVersionsResponse(ResponseWithMeta):
    '''Ответ со списком версий kubernetes

    Attributes:
        k8s_versions (list[str]): Объект со списком версий kubernetes
    '''
    k8s_versions: list[str]


class K8SNetworksResponse(ResponseWithMeta):
    '''Ответ со списком сетевых драйверов kubernetes

    Attributes:
        network_drivers (list[str]): Список сетевых драйверов kubernetes
    '''
    network_drivers: list[str]


class K8SPreset(BaseData):
    '''Модель тарифа kubernetes

    Attributes:
        id (int): Уникальный идентификатор тарифа
        description (str): Описание тарифа
        description_short (str): Краткое описание тарифа
        price (Decimal): Стоимость
        cpu (int): Количество ядер ноды
        ram (int): Количество памяти ноды
        disk (int): Количество пространства на ноде
        network (int): Пропускная способность ноды
        type (str | None): Тип тарифа
    '''
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
    '''Ответ со списком тарифов для kubernetes.

    Attributes:
        k8s_presets (list[K8SPreset]): Список тарифов для kubernetes
    '''
    k8s_presets: list[K8SPreset]
