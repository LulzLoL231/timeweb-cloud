# -*- coding: utf-8 -*-
'''Модели для работы с заявками над доменами.'''
from datetime import datetime

from ..time_utils import Period
from ..base import ResponseWithMeta, BaseResponse, BaseData


class DomainRequest(BaseData):
    '''Модель данных о заявки над доменом.

    Attributes:
        account_id (str): Идентификатор пользователя
        auth_code (str | None): Код авторизации для переноса домена.
        date (datetime): Дата создания заявки.
        domain_bundle_id (str | None): Идентификационный номер бандла, в который входит данная заявка (null - если заявка не входит ни в один бандл).
        error_code_transfer (str | None): Код ошибки трансфера домена.
        fqdn (str): Полное имя домена.
        group_id (int): Идентификатор группы доменных зон.
        id (int): Идентификатор заявки.
        is_antispam_enabled (bool): Это логическое значение, которое показывает включена ли услуга "Антиспам" для домена
        is_autoprolong_enabled (bool | None): Это логическое значение, которое показывает, включено ли автопродление домена.
        is_whois_privacy_enabled (bool): Это логическое значение, которое показывает, включено ли скрытие данных администратора домена для whois. Опция недоступна для доменов в зонах .ru и .рф.
        message (str | None): Информационное сообщение о заявке.
        money_source (str | None): Источник (способ) оплаты заявки.
        period (Period): Период оплаты (Для доменов в зонах .ru и .рф только 1-3 года).
        person_id (int): Идентификационный номер персоны для заявки на регистрацию.
        prime (str | None): Тип прайм домена.
        soon_expire (int): Количество дней до конца регистрации домена, за которые мы уведомим о необходимости продления.
        sort_order (int): Это значение используется для сортировки доменных зон в панели управления.
        type (str): Тип заявки.
    '''
    account_id: str
    auth_code: str | None
    date: datetime
    domain_bundle_id: str | None
    error_code_transfer: str | None
    fqdn: str
    group_id: int
    id: int
    is_antispam_enabled: bool
    is_autoprolong_enabled: bool | None
    is_whois_privacy_enabled: bool
    message: str | None
    money_source: str | None
    period: Period
    person_id: int
    prime: str | None
    soon_expire: int
    sort_order: int
    type: str


class DomainsRequestsResponse(ResponseWithMeta):
    '''Ответ со списком заявок к доменам.

    Attributes:
        requests (list[DomainRequest]): Список заявок к доменам.
    '''
    requests: list[DomainRequest]


class DomainRequestResponse(BaseResponse):
    '''Ответ с заявкой к домену.

    Attributes:
        request (DomainRequest): Заявка к домену.
    '''
    request: DomainRequest
