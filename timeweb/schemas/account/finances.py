# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import datetime

from pydantic import Field, BaseModel

from ..base import BaseResponse


class Finances(BaseModel):
    '''Платежная информация

    Attributes:
        balance (Decimal): Баланс аккаунта.
        currency (str): Валюта, которая используется на аккаунте.
        discount_end_date_at (datetime | None): Дата окончания скидки для аккаунта.
        discount_percent (int): Процент скидки для аккаунта.
        hourly_cost (Decimal): Стоимость услуг на аккаунте в час.
        hourly_fee (Decimal): Абонентская плата в час (с учетом скидок).
        monthly_cost (Decimal): Стоимость услуг на аккаунте в месяц.
        monthly_fee (Decimal): Абонентская плата в месяц (с учетом скидок).
        total_paid (int): Общая сумма платежей на аккаунте.
        hours_left (int | None): Сколько часов работы услуг оплачено на аккаунте.
        autopay_card_info (str | None): Информация о карте, используемой для автоплатежей.
    '''
    balance: Decimal = Field(..., description='Баланс аккаунта.')
    currency: str = Field(...,
                          description='Валюта, которая используется на аккаунте.')
    discount_end_date_at: datetime | None = Field(
        None, description='Дата окончания скидки для аккаунта.'
    )
    discount_percent: int = Field(...,
                                  description='Процент скидки для аккаунта.')
    hourly_cost: Decimal = Field(...,
                                 description='Стоимость услуг на аккаунте в час.')
    hourly_fee: Decimal = Field(...,
                                description='Абонентская плата в час (с учетом скидок).')
    monthly_cost: Decimal = Field(...,
                                  description='Стоимость услуг на аккаунте в месяц.')
    monthly_fee: Decimal = Field(...,
                                 description='Абонентская плата в месяц (с учетом скидок).')
    total_paid: int = Field(...,
                            description='Общая сумма платежей на аккаунте.')
    hours_left: int | None = Field(
        None, description='Сколько часов работы услуг оплачено на аккаунте.')
    autopay_card_info: str | None = Field(
        None, description='Информация о карте, используемой для автоплатежей.')


class AccountFinances(BaseResponse):
    '''Платежная информация

    Attributes:
        finances (Finances): Платежная информация.
    '''
    finances: Finances = Field(..., description='Платежная информация.')
