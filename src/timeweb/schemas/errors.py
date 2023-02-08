# -*- coding: utf-8 -*-
from pydantic import Field

from .base import BaseResponse


class BaseError(BaseResponse):
    '''Базовая модель ошибки'''
    status_code: int = Field(
        ..., description='Короткий числовой идентификатор ошибки.'
    )
    error_code: str = Field(
        ..., description=('Короткий текстовый идентификатор ошибки, '
                          'который уточняет числовой идентификатор и удобен '
                          'для программной обработки.')
    )
    message: str | list[str] | None = Field(
        None, description=('В большинстве случаев в ответе будет содержаться '
                           'человекочитаемое подробное описание ошибки или ошибок, '
                           'которые помогут понять, что нужно исправить.')
    )
