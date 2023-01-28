# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field, BaseModel

from ..base import BaseResponse


class CompanyInfo(BaseModel):
    '''Информация о компании.

    Attributes:
        id (int): Идентификатор компании.
        name (str): Название компании.
    '''
    id: int = Field(..., description='Идентификатор компании.')
    name: str = Field(..., description='Название компании.')


class Status(BaseModel):
    '''Статус аккаунта.

    Attributes:
        is_blocked (bool): Заблокирован ли аккаунт.
        is_permanent_blocked (bool): Заблокирован ли аккаунт навсегда.
        company_info (CompanyInfo): Информация о компании.
        last_password_changed_at (datetime): Дата последней смены пароля.
        ym_client_id (str | None): Идентификатор клиента в Яндекс.Метрике.
    '''
    is_blocked: bool = Field(..., description='Заблокирован ли аккаунт.')
    is_permanent_blocked: bool = Field(
        ..., description='Заблокирован ли аккаунт навсегда.'
    )
    is_send_bill_letters: bool = Field(
        ..., description='Отправляются ли счета на почту.'
    )
    company_info: CompanyInfo = Field(
        ..., description='Информация о компании.'
    )
    last_password_changed_at: datetime = Field(
        ..., description='Дата последней смены пароля.'
    )
    ym_client_id: str | None = Field(
        None, description='Идентификатор клиента в Яндекс.Метрике.'
    )


class AccountStatus(BaseResponse):
    '''Статус аккаунта.

    Attributes:
        status (Status): Статус аккаунта.
    '''
    status: Status = Field(..., description='Статус аккаунта.')
