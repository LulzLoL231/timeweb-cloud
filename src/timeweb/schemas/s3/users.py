# -*- coding: utf-8 -*-
'''Модели для работы с S3 пользователями'''
from pydantic import BaseModel, Field

from ..base import ResponseWithMeta, BaseResponse


class User(BaseModel):
    '''Модель пользователя S3-хранилища'''
    id: int = Field(..., description='ID пользователя')
    access_key: str = Field(..., description='Ключ доступа пользователя')
    secret_key: str = Field(...,
                            description='Секретный ключ доступа пользователя')


class StorageUsers(ResponseWithMeta):
    '''Модель ответа со списком пользователей S3-хранилищ'''
    users: list[User]


class UserResponse(BaseResponse):
    '''Модель ответа с пользователем S3-хранилища'''
    user: User
