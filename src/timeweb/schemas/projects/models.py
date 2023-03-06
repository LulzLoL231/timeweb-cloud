# -*- coding: utf-8 -*-
'''Модели для работы с проектами'''
from datetime import datetime

from ..base import BaseData


class Project(BaseData):
    '''Модель проекта'''
    id: int
    account_id: str
    avatar_id: str | None
    description: str
    name: str
    is_default: bool


class Resource(BaseData):
    '''Модель ресурса проекта'''
    id: int
    created_at: datetime
    resource_id: int
    project: Project
    type: str
