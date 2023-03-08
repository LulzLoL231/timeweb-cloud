# -*- coding: utf-8 -*-
'''Модели для работы с S3 пользователями'''
from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData


class User(BaseData):
    '''Модель пользователя S3-хранилища.

    Attributes:
        id (int): ID пользователя
        access_key (str): Ключ доступа пользователя
        secret_key (str): Секретный ключ доступа пользователя
    '''
    id: int = Field(..., description='ID пользователя')
    access_key: str = Field(..., description='Ключ доступа пользователя')
    secret_key: str = Field(...,
                            description='Секретный ключ доступа пользователя')


class StorageUsers(ResponseWithMeta):
    '''Модель ответа со списком пользователей S3-хранилищ.

    Attributes:
        users (list[User]): Список пользователей хранилищ
    '''
    users: list[User]


class UserResponse(BaseResponse):
    '''Модель ответа с пользователем S3-хранилища.

    Attributes:
        user (User): Пользователь хранилища.
    '''
    user: User
