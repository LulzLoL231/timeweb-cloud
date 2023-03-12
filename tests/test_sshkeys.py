# -*- coding: utf-8 -*-
from timeweb import Timeweb
from timeweb.schemas import ssh_keys as schemas
from timeweb.schemas.ssh_keys.ssh_keys import SSHKey


KEY_NAME = 'TESTKEY_PYTEST'
KEY_NEWNAME = 'TESTKEY_PYTEST_NEW'


def search_key(name: str, ssh_keys: list[SSHKey]) -> SSHKey:
    array = list(
        filter(lambda t: t.name == name, ssh_keys)
    )
    return array.pop(0)


def test_get_keys(tw: Timeweb):
    keys = tw.ssh_keys.get_keys()
    assert isinstance(keys, schemas.SSHKeysArray)


def test_create_key(tw: Timeweb, test_ssh_key: str):
    key = tw.ssh_keys.create(KEY_NAME, test_ssh_key, False)
    assert isinstance(key, schemas.CreateSSHKeyResponse)
    assert key.ssh_key.name == KEY_NAME
    assert key.ssh_key.body == test_ssh_key


def test_get_key(tw: Timeweb, test_ssh_key: str):
    keys = tw.ssh_keys.get_keys()
    found_key = search_key(KEY_NAME, keys.ssh_keys)
    key = tw.ssh_keys.get(found_key.id)
    assert isinstance(key, schemas.SSHKeyResponse)
    assert key.ssh_key.id == found_key.id
    assert key.ssh_key.name == KEY_NAME
    assert key.ssh_key.body == test_ssh_key


def test_update_key(tw: Timeweb):
    keys = tw.ssh_keys.get_keys()
    found_key = search_key(KEY_NAME, keys.ssh_keys)
    updated = tw.ssh_keys.update(found_key.id, KEY_NEWNAME)
    assert found_key.id == updated.ssh_key.id
    assert found_key.name != updated.ssh_key.name
    assert updated.ssh_key.name == KEY_NEWNAME


def test_delete_key(tw: Timeweb):
    keys = tw.ssh_keys.get_keys()
    found_key = search_key(KEY_NEWNAME, keys.ssh_keys)
    status = tw.ssh_keys.delete(found_key.id)
    assert status is True
