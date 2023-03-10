# -*- coding: utf-8 -*-
import httpx
import pytest
from pydantic import BaseSettings, Field

from timeweb import Timeweb


IP_SERVICES = [
    'http://checkip.amazonaws.com',
    'http://ifconfig.co/ip'
]


class Config(BaseSettings):
    token: str = Field(..., env='TIMEWEB_TOKEN')

    class Config:
        env_file = 'tests/.env'


@pytest.fixture()
def tw():
    cfg = Config()
    return Timeweb(cfg.token)


@pytest.fixture()
def my_ip() -> str:
    for srv in IP_SERVICES:
        try:
            resp = httpx.get(srv)
        except Exception:
            continue
        else:
            if resp.is_success:
                return resp.text.strip()
    raise RuntimeError('Can\'t fetch IP address!')
