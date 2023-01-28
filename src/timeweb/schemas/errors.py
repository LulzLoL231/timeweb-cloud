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


# class BadRequestError(BaseError):
#     '''Был отправлен неверный запрос, например, в нем отсутствуют обязательные параметры и т. д. Тело ответа будет содержать дополнительную информацию об ошибке.'''
#     status_code = 400
#     error_code = 'bad_request'


# class UnauthorizedError(BaseError):
#     '''Ошибка аутентификации.'''
#     status_code = 401
#     error_code = 'unauthorized'


# class ForbiddenError(BaseError):
#     '''Аутентификация прошла успешно, но не достаточно прав для выполнения действия.'''
#     status_code = 403
#     error_code = 'forbidden'


# class NotFoundError(BaseError):
#     '''Запрашиваемый ресурс не найден.'''
#     status_code = 404
#     error_code = 'not_found'


# class ConflictError(BaseError):
#     '''Запрос не может быть выполнен из-за конфликта с текущим состоянием ресурса.'''
#     status_code = 409
#     error_code = 'conflict'


# class LockedError(BaseError):
#     '''Ресурс из запроса заблокирован от применения к нему указанного метода.'''
#     status_code = 423
#     error_code = 'locked'


# class TooManyRequestsError(BaseError):
#     '''Был достигнут лимит по количеству запросов в единицу времени.'''
#     status_code = 429
#     error_code = 'too_many_requests'


# class InternalServerError(BaseError):
#     '''При выполнении запроса произошла какая-то внутренняя ошибка. Чтобы решить эту проблему лучше всего создать тикет в панели управления.'''
#     status_code = 500
#     error_code = 'internal_server_error'
