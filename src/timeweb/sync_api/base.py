# -*- coding: utf-8 -*-
import sys
import logging

from httpx import Client, Response, HTTPStatusError

from ..errors import exc
from ..__meta import __version__
from ..schemas.errors import BaseError


class BaseClient:
    '''Базовый клиент для синхронной работы с Timeweb Cloud API.'''
    BASE_URL = 'https://api.timeweb.cloud/api/v1/'

    def __init__(
        self, token: str, client: Client | None = None
    ):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        self.log = logging.getLogger('timeweb')
        self.token = token
        ua = f'timeweb-cloud/{__version__} (Python {sys.version}) '
        ua += 'https://github.com/LulzLoL231/timeweb-cloud'
        default_client = Client(
            headers={
                'User-Agent': f'timeweb-cloud/{__version__}',
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/json'
            }, base_url=self.BASE_URL
        )
        self.client = client or default_client

    def _request(
        self, method: str, url: str, **kwargs
    ) -> Response:
        '''Отправка запроса к API.

        Args:
            method (str): HTTP метод.
            url (str): URL запроса.

        Raises:
            exc.BadRequestError: Был отправлен неверный запрос, например, в нем отсутствуют обязательные параметры и т. д. Тело ответа будет содержать дополнительную информацию об ошибке.
            exc.UnauthorizedError: Ошибка аутентификации.
            exc.ForbiddenError: Аутентификация прошла успешно, но не достаточно прав для выполнения действия.
            exc.NotFoundError: Запрашиваемый ресурс не найден.
            exc.ConflictError: Запрос не может быть выполнен из-за конфликта с текущим состоянием ресурса.
            exc.LockedError: Ресурс из запроса заблокирован от применения к нему указанного метода.
            exc.TooManyRequestsError: Был достигнут лимит по количеству запросов в единицу времени.
            exc.InternalServerError: При выполнении запроса произошла какая-то внутренняя ошибка. Чтобы решить эту проблему лучше всего создать тикет в панели управления.
            exc.UnexpectedError: Неизвестная ошибка от API.
            exc.ResponseMalformedError: Ответ от API не соответствует ожидаемому формату.

        Returns:
            Response: Httpx response.
        '''
        self.log.debug(f'Called with args: ({method}, {url})')
        response = self.client.request(method, url, **kwargs)
        self.log.debug(f'Response: {response.text}')
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            try:
                error = BaseError(**e.response.json())
            except Exception as json_err:
                self.log.error(f'Malformed error response: {e.response.text}', exc_info=json_err)
                raise exc.ResponseMalformedError(e.request, e.response)
            match error.status_code:
                case 400:
                    raise exc.BadRequestError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 401:
                    raise exc.UnauthorizedError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 403:
                    raise exc.ForbiddenError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 404:
                    raise exc.NotFoundError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 409:
                    raise exc.ConflictError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 423:
                    raise exc.LockedError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 429:
                    raise exc.TooManyRequestsError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case 500:
                    raise exc.InternalServerError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
                case _:
                    raise exc.UnexpectedError(
                        request=e.request,
                        response=e.response,
                        message=error.message,
                        response_id=error.response_id
                    )
        else:
            return response
