# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from timeweb import Timeweb
from timeweb.schemas import tokens as schemas
from timeweb.schemas.tokens.api_keys import APIKey


TOKEN_NAME = 'TESTTOKEN_PYTEST'
TOKEN_NEWNAME = 'TESTTOKEN_PYTEST_NEW'


def search_token(name: str, api_keys: list[APIKey]) -> APIKey:
    array = list(
        filter(lambda t: t.name == name, api_keys)
    )
    return array.pop(0)


def test_get_tokens(tw: Timeweb):
    tokens = tw.tokens.get_tokens()
    assert isinstance(tokens, schemas.APIKeysResponse)


def test_create(tw: Timeweb):
    next_day = datetime.now() + timedelta(days=1)
    created = tw.tokens.create(TOKEN_NAME, next_day)
    assert isinstance(created, schemas.CreateAPIKeyResponse)
    assert created.api_key.expired_at.date() == next_day.date()


def test_rename(tw: Timeweb):
    token = search_token(TOKEN_NAME, tw.tokens.get_tokens().api_keys)
    new_token = tw.tokens.rename(token.id, TOKEN_NEWNAME)
    assert new_token.api_key.id == token.id
    assert new_token.api_key.name == TOKEN_NEWNAME


def test_reissue(tw: Timeweb):
    token = search_token(TOKEN_NEWNAME, tw.tokens.get_tokens().api_keys)
    next_mon = datetime.now() + timedelta(days=30)
    new_token = tw.tokens.reissue(token.id, next_mon)
    assert isinstance(new_token, schemas.CreateAPIKeyResponse)
    assert new_token.api_key.expired_at.date() == next_mon.date()


def test_delete(tw: Timeweb):
    token = search_token(TOKEN_NEWNAME, tw.tokens.get_tokens().api_keys)
    status = tw.tokens.delete(token.id)
    assert status is True
    tokens = tw.tokens.get_tokens().api_keys
    tokens_ids = list(filter(lambda t: t.id.hex, tokens))
    assert token.id.hex not in tokens_ids
