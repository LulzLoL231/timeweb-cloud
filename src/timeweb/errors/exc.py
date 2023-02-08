# -*- coding: utf-8 -*-
'''Исключения для библиотеки'''
from uuid import UUID

from httpx import HTTPStatusError, Request, Response


class TimewebError(HTTPStatusError):
    '''Базовое исключение Timeweb Cloud API'''
    def __init__(
        self,
        request: "Request",
        response: "Response",
        message: str | list[str] | None = None,
        response_id: UUID | str | None = None
    ) -> None:
        if message is not None:
            if isinstance(message, list):
                description = '; '.join(message)
            else:
                description = message
        else:
            description = response.reason_phrase
        super().__init__(message=description, request=request, response=response)
        self.response_id = response_id


class BadRequestError(TimewebError):
    '''Был отправлен неверный запрос, например, в нем отсутствуют обязательные параметры и т. д. Тело ответа будет содержать дополнительную информацию об ошибке.
    '''
    pass


class UnauthorizedError(TimewebError):
    '''Ошибка аутентификации.'''
    pass


class ForbiddenError(TimewebError):
    '''Аутентификация прошла успешно, но не достаточно прав для выполнения действия.'''
    pass


class NotFoundError(TimewebError):
    '''Запрашиваемый ресурс не найден.'''
    pass


class ConflictError(TimewebError):
    '''Запрос конфликтует с текущим состоянием.'''
    pass


class LockedError(TimewebError):
    '''Ресурс из запроса заблокирован от применения к нему указанного метода.'''
    pass


class TooManyRequestsError(TimewebError):
    '''Был достигнут лимит по количеству запросов в единицу времени.'''
    pass


class InternalServerError(TimewebError):
    '''При выполнении запроса произошла какая-то внутренняя ошибка. Чтобы решить эту проблему лучше всего создать тикет в панели управления.
    '''
    pass


class UnexpectedError(TimewebError):
    '''Неизвестная ошибка.'''
    pass


class ResponseMalformedError(TimewebError):
    '''Неверный формат ответа.'''
    pass
