# -*- coding: utf-8 -*-
# flake8: noqa
'''Модели для работы с доменами.'''
from .domains import (
    DomainsResponse, DomainResponse, SubdomainResponse,
    DomainAvailability
)
from .tld import (
    TLDomainResponse, TLDomainsResponse
)
from .requests import (
    DomainsRequestsResponse, DomainRequestResponse
)
from .ns import (
    NameServersResponse
)
from .dns import (
    DNSRecordResponse, DNSRecordsResponse
)
