# -*- coding: utf-8 -*-
'''Модели для работы с логами облачного сервера'''
from datetime import datetime

from ...base import ResponseWithMeta, BaseData


class ServerLog(BaseData):
    '''Событие сервера.

    Attributes:
        id (int): Уникальный идентификатор диска.
        logged_at (datetime): Дата лога
        event (str): Событие сервера
    '''
    id: int
    logged_at: datetime
    event: str


class ServerLogsResponse(ResponseWithMeta):
    '''Ответ со списком событий серверов.

    Attributes:
        server_logs (list[ServerLog]): Список событий сервера.
    '''
    server_logs: list[ServerLog]
