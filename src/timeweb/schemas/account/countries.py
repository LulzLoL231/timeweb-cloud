# -*- coding: utf-8 -*-
from enum import Enum
from typing import Dict

from pydantic import Field, BaseModel

from ..base import BaseResponse


class RestrictionsStatus(BaseModel):
    is_enabled: bool = Field(..., description='Включены ли ограничения.')


class AccessCountries(BaseResponse):
    '''Список доступных стран.

    Attributes:
        countries (Dict[str, str]): Список стран, приходит в виде объекта, где ключ - код страны в формате Alpha-2 ISO 3166-1, а значение - название страны в удобочитаемом формате.
    '''
    countries: Dict[str, str] = Field(
        ..., description=('Список стран, приходит в виде объекта, '
                          'где ключ - код страны в формате Alpha-2 ISO 3166-1, '
                          'а значение - название страны в удобочитаемом формате.')
    )


class AddAccessCountriesStatus(str, Enum):
    '''Результат добавления страны.

    Attributes:
        success (str): Успешно.
        conflict (str): Страна уже добавлена.
    '''
    SUCCESS = 'success'
    CONFLICT = 'conflict'


class AddedCountries(BaseModel):
    '''Статус добавленния страны.

    Attributes:
        value (str): Код страны в формате Alpha-2 ISO 3166-1.
        status (AddAccessCountriesStatus): Статус добавления страны.
    '''
    value: str = Field(..., description='Код страны в формате Alpha-2 ISO 3166-1.')
    status: AddAccessCountriesStatus = Field(..., description='Статус добавления страны.')


class AddAccessCountries(BaseResponse):
    '''Список добавленных стран.

    Attributes:
        countries (list[AddedCountries]): Статус добавленния стран.
    '''
    countries: list[AddedCountries] = Field(
        ..., description='Статус добавленния стран.'
    )


class RemoveAccessCountriesStatus(str, Enum):
    '''Результат удаления страны.

    Attributes:
        success (str): Успешно.
        not_found (str): Страна не найдена.
    '''
    SUCCESS = 'success'
    NOT_FOUND = 'not_found'


class RemovedCountries(BaseModel):
    '''Статус удаления страны.

    Attributes:
        value (str): Код страны в формате Alpha-2 ISO 3166-1.
        status (RemoveAccessCountriesStatus): Статус удаления страны.
    '''
    value: str = Field(..., description='Код страны в формате Alpha-2 ISO 3166-1.')
    status: AddAccessCountriesStatus = Field(..., description='Статус удаления страны.')


class RemoveAccessCountries(BaseResponse):
    '''Список удаленных стран.

    Attributes:
        countries (list[RemovedCountries]): Статус удаления стран.
    '''
    countries: list[RemovedCountries] = Field(
        ..., description='Статус удаления стран.'
    )
