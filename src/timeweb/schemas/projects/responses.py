# -*- coding: utf-8 -*-
'''Модели для работы с проектами'''
from ..base import ResponseWithMeta, BaseResponse
from ..servers.cloud.cloud import VDS
from ..balancers.balancers import Balancer
from ..s3.s3 import Bucket
from ..kubernetes.kubernetes import Cluster
from ..dbs.dbs import Database
from ..servers.dedics.dedics import DedicatedServer

from .models import Project, Resource


class ResourcesResponse(ResponseWithMeta):
    '''Ответ с ресурсами проекта'''
    servers: list[VDS]
    balancers: list[Balancer]
    buckets: list[Bucket]
    clusters: list[Cluster]
    databases: list[Database]
    dedicated_servers: list[DedicatedServer]


class ProjectsResponse(ResponseWithMeta):
    '''Ответ со списком проектов'''
    projects: list[Project]


class ProjectResponse(BaseResponse):
    '''Ответ с проектом'''
    project: Project


class ResourceResponse(BaseResponse):
    '''Ответ с ресурсом проекта'''
    resource: Resource
