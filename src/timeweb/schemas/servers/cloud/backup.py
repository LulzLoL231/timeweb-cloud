# -*- coding: utf-8 -*-
'''Модели для работы с бэкапами облачного сервера'''
from datetime import date, datetime

from ...base import ResponseWithMeta, BaseData, BaseResponse


class AutoBackup(BaseData):
    '''Настройки авто-бэкапа сервера.

    Attributes:
        copy_count (int | None): Количество копий для хранения. Минимальное количество 1, максимальное 99
        creation_start_at (date | None): Дата начала создания первого автобэкапа.
        is_enabled (bool): Включено ли автобэкапирование
        interval (str | None): Периодичность создания автобэкапов
        day_of_week (int | None): День недели, в который будут создаваться автобэкапы. Работает только со значением `interval`: `week`. Доступные значение от 1 до 7.
    '''
    copy_count: int | None
    creation_start_at: date | None
    is_enabled: bool
    interval: str | None
    day_of_week: int | None


class AutoBackupsResponse(BaseResponse):
    '''Ответ с настройками авто-бэкапов облачного сервера.

    Attributes:
        auto_backups_settings (AutoBackup): Настройки авто-бэкапов облачного сервера
    '''
    auto_backups_settings: AutoBackup


class Backup(BaseData):
    '''Объект бэкапа.

    Attributes:
        id (int): Уникальный идентификатор бэкапа сервера.
        name (str): Название бэкапа.
        comment (str | None): Комментарий к бэкапу.
        created_at (datetime): Дата создания бэкапа.
        status (str): Статус бэкапа.
        size (int): Размер бэкапа (в Мб).
        type (str): Тип бэкапа.
    '''
    id: int
    name: str
    comment: str | None
    created_at: datetime
    status: str
    size: int
    type: str


class BackupsResponse(ResponseWithMeta):
    '''Ответ со списком бэкапов.

    Attributes:
        backups (list[Backup]): Список бэкапов.
    '''
    backups: list[Backup]


class BackupResponse(BaseResponse):
    '''Ответ с бэкапом.

    Attributes:
        backup (Backup): Бэкап.
    '''
    backup: Backup
