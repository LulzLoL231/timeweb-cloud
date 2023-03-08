# -*- coding: utf-8 -*-
'''Модели для работы с Базами данных'''
from enum import Enum
from datetime import datetime
from ipaddress import IPv4Address

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData, BaseDelete


class DBType(str, Enum):
    '''Типы Баз данных

    Attributes:
        MySQL (str): mysql
        MySQL5 (str): mysql5
        PostgreSQL (str): postgresql
        Redis (str): redis
        MondoDB (str): mongodb
    '''
    MySQL = 'mysql'
    MySQL5 = 'mysql5'
    PostgreSQL = 'postgresql'
    Redis = 'redis'
    MondoDB = 'mongodb'


class DBHashType(str, Enum):
    '''Типы хэшей Баз данных

    Attributes:
        CACHING_SHA2 (str): caching_sha2
        MySQL_Native (str): mysql_native
    '''
    CACHING_SHA2 = 'caching_sha2'
    MySQL_Native = 'mysql_native'


class DBStatus(str, Enum):
    '''Статусы Баз данных

    Attributes:
        STARTED (str): started
        STARTING (str): starting
        STOPED (str): stoped
        NO_PAID (str): no_paid
    '''
    STARTED = 'started'
    STARTING = 'starting'
    STOPED = 'stoped'
    NO_PAID = 'no_paid'


class DBDiskStats(BaseData):
    '''Статистика диска

    Attributes:
        size (int): Размер (в Кб) диска базы данных.
        used (int): Размер(в Кб) использованного пространства диска базы данных.
    '''
    size: int = Field(..., description='Размер (в Кб) диска базы данных.')
    used: int = Field(
        ..., description='Размер(в Кб) использованного пространства диска базы данных.'
    )


class DBConfigParameters(BaseData):
    '''Параметры конфигурации Базы данных

    Attributes:
        auto_increment_increment (str | None): Интервал между значениями столбцов с атрибутом.
        auto_increment_offset (str | None): Начальное значение для столбцов с атрибутом "AUTO_INCREMENT".
        innodb_io_capacity (str | None): Количество потоков ввода-вывода, используемых для операций очистки.
        innodb_read_io_threads (str | None): Максимальное число потоков, которые могут исполняться.
        innodb_write_io_threads (str | None): Количество потоков ввода-вывода, используемых для операций записи.
        join_buffer_size (str | None): Минимальный размер буфера.
        max_allowed_packet (str | None): Максимальный размер одного пакета, строки или параметра, отправляемого функцией "mysql_stmt_send_long_data()".
        max_heap_table_size (str | None): 'Максимальный размер пользовательских MEMORY-таблиц.
        autovacuum_analyze_scale_factor (str | None): Доля измененных или удаленных записей в таблице, при которой процесс автоочистки выполнит команду "ANALYZE".
        bgwriter_delay (str | None): Задержка между запусками процесса фоновой записи.
        bgwriter_lru_maxpages (str | None): Максимальное число элементов буферного кеша.
        deadlock_timeout (str | None): Время ожидания, по истечении которого будет выполняться проверка состояния перекрестной блокировки.
        gin_pending_list_limit (str | None): Максимальный размер очереди записей индекса "GIN".
        idle_in_transaction_session_timeout (str | None): Время простоя открытой транзакции, при превышении которого будет завершена сессия с этой транзакцией.
        idle_session_timeout (str | None): Время простоя не открытой транзакции, при превышении которого будет завершена сессия с этой транзакцией.
        join_collapse_limit (str | None): Значение количества элементов в списке "FROM" при превышении которого, планировщик будет переносить в список явные инструкции "JOIN".
        lock_timeout (str | None): Время ожидания освобождения блокировки.
        max_prepared_transactions (str | None): Максимальное число транзакций, которые могут одновременно находиться в подготовленном состоянии.
    '''
    auto_increment_increment: str | None = Field(
        None, description='Интервал между значениями столбцов с атрибутом.'
    )
    auto_increment_offset: str | None = Field(
        None, description='Начальное значение для столбцов с атрибутом "AUTO_INCREMENT".'
    )
    innodb_io_capacity: str | None = Field(
        None, description='Количество потоков ввода-вывода, используемых для операций очистки.'
    )
    innodb_read_io_threads: str | None = Field(
        None, description='Максимальное число потоков, которые могут исполняться.'
    )
    innodb_write_io_threads: str | None = Field(
        None, description='Количество потоков ввода-вывода, используемых для операций записи.'
    )
    join_buffer_size: str | None = Field(
        None, description='Минимальный размер буфера.'
    )
    max_allowed_packet: str | None = Field(
        None, description='Максимальный размер одного пакета, строки или параметра, отправляемого функцией "mysql_stmt_send_long_data()".'
    )
    max_heap_table_size: str | None = Field(
        None, description='Максимальный размер пользовательских MEMORY-таблиц.'
    )
    autovacuum_analyze_scale_factor: str | None = Field(
        None, description='Доля измененных или удаленных записей в таблице, при которой процесс автоочистки выполнит команду "ANALYZE".'
    )
    bgwriter_delay: str | None = Field(
        None, description='Задержка между запусками процесса фоновой записи.'
    )
    bgwriter_lru_maxpages: str | None = Field(
        None, description='Максимальное число элементов буферного кеша.'
    )
    deadlock_timeout: str | None = Field(
        None, description='Время ожидания, по истечении которого будет выполняться проверка состояния перекрестной блокировки.'
    )
    gin_pending_list_limit: str | None = Field(
        None, description='Максимальный размер очереди записей индекса "GIN".'
    )
    idle_in_transaction_session_timeout: str | None = Field(
        None, description='Время простоя открытой транзакции, при превышении которого будет завершена сессия с этой транзакцией.'
    )
    idle_session_timeout: str | None = Field(
        None, description='Время простоя не открытой транзакции, при превышении которого будет завершена сессия с этой транзакцией.'
    )
    join_collapse_limit: str | None = Field(
        None, description='Значение количества элементов в списке "FROM" при превышении которого, планировщик будет переносить в список явные инструкции "JOIN".'
    )
    lock_timeout: str | None = Field(
        None, description='Время ожидания освобождения блокировки.'
    )
    max_prepared_transactions: str | None = Field(
        None, description='Максимальное число транзакций, которые могут одновременно находиться в подготовленном состоянии.'
    )


class Database(BaseData):
    '''Модель базы данных

    Attributes:
        id (int): Уникальный идентификатор для каждого экземпляра базы данных
        created_at (datetime): Дата создания базы данных
        account_id (str): Идентификатор пользователя
        login (str): Логин для подключения к базе данных.
        password (str): Пароль для подключения к базе данных.
        name (str): Имя базы данных.
        host (str): Хост базы данных.
        type (DBType): Тип базы данных.
        hash_type (DBHashType): Тип хеширования базы данных (mysql5 | mysql | postgres).
        port (int): Порт базы данных.
        ip (IPv4Address | None): IP-адрес сетевого интерфейса IPv4.
        local_ip (IPv4Address | None): IP-адрес локального сетевого интерфейса IPv4.
        status (DBStatus): Статус базы данных.
        preset_id (int): Идентификатор тарифа.
        dist_stats (DBDiskStats | None): Статистика использования диска базы данных.
        config_parameters (DBConfigParameters): Параметры конфигурации базы данных.
        is_only_local_ip_access (bool): Доступна ли база данных только по локальному IP адресу.
    '''
    id: int = Field(
        ..., description='Уникальный идентификатор для каждого экземпляра базы данных'
    )
    created_at: datetime = Field(..., description='Дата создания базы данных')
    account_id: str = Field(..., description='Идентификатор пользователя')
    login: str = Field(..., description='Логин для подключения к базе данных.')
    password: str = Field(...,
                          description='Пароль для подключения к базе данных.')
    name: str = Field(..., description='Имя базы данных.')
    host: str = Field(..., description='Хост базы данных.')
    type: DBType = Field(..., description='Тип базы данных.')
    hash_type: DBHashType = Field(
        ..., description='Тип хеширования базы данных (mysql5 | mysql | postgres).'
    )
    port: int = Field(..., description='Порт базы данных.')
    ip: IPv4Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPv4.')
    local_ip: IPv4Address | None = Field(
        None, description='IP-адрес локального сетевого интерфейса IPv4.')
    status: DBStatus = Field(..., description='Статус базы данных.')
    preset_id: int = Field(..., description='Идентификатор тарифа.')
    dist_stats: DBDiskStats | None = Field(
        None, description='Статистика использования диска базы данных.'
    )
    config_parameters: DBConfigParameters = Field(
        ..., description='Параметры конфигурации базы данных.'
    )
    is_only_local_ip_access: bool = Field(
        ..., description='Доступна ли база данных только по локальному IP адресу.'
    )


class DBArray(ResponseWithMeta):
    """Ответ со списком баз данных.

    Attributes:
        dbs (list[Database]): Массив баз данных.
    """
    dbs: list[Database] = Field(..., description='Массив баз данных.')


class DatabaseResponse(BaseResponse):
    """Ответ с базой данных.

    Attributes:
        db (Database): База данных.
    """
    db: Database = Field(..., description='База данных.')


class DatabaseDelete(BaseResponse):
    '''Ответ с хэшом для подтверждения удаления БД

    database_delete (BaseDelete): Хэщ для подтверждения удаления БД'''
    database_delete: BaseDelete
