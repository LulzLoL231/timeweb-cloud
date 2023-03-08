# -*- coding: utf-8 -*-
'''Модели для работы с проектами'''
from datetime import datetime

from ..base import BaseData


class Project(BaseData):
    '''Модель проекта.

    Attributes:
        id (int): Уникальный идентификатор для каждого проекта. Автоматически генерируется при создании.
        account_id (str): Идентификатор пользователя.
        avatar_id (str | None): Идентификатор аватара пользователя. Описание методов работы с аватарами появится позднее.
        description (str): Описание проекта.
        name (str): Удобочитаемое имя проекта.
        is_default (bool): Это логическое значение, которое показывает, выбран ли проект по умолчанию для создания новых сущностей.
    '''
    id: int
    account_id: str
    avatar_id: str | None
    description: str
    name: str
    is_default: bool


class Resource(BaseData):
    '''Модель ресурса проекта.

    Attributes:
        id (int): Уникальный идентификатор для каждого ресурса проекта. Автоматически генерируется при создании.
        created_at (datetime): Значение времени, указанное в комбинированном формате даты и времени ISO8601, которое представляет, когда был создан ресурс.
        resource_id (int): Идентификатор ресурса проекта (сервера, хранилища, кластера, балансировщика, базы данных или выделенного сервера).
        project (Project): Проект
        type (str): Тип ресурса проекта
    '''
    id: int
    created_at: datetime
    resource_id: int
    project: Project
    type: str
