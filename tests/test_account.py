# -*- coding: utf-8 -*-
from timeweb import Timeweb
from timeweb.schemas import account as schemas


def test_get_finances(tw: Timeweb):
    finances = tw.account.get_finances()
    assert isinstance(finances, schemas.AccountFinances)


def test_get_status(tw: Timeweb):
    status = tw.account.get_status()
    assert isinstance(status, schemas.AccountStatus)


class TestAccessRestrictions:
    def test_get_access_restrictions(self, tw: Timeweb):
        rests = tw.account.get_access_restrictions()
        assert isinstance(rests, schemas.AccountAccess)

    def test_turn_countries_restrictions(self, tw: Timeweb):
        current_rests = tw.account.get_access_restrictions()
        change_status = tw.account.turn_countries_restrictions(not current_rests.is_country_restrictions_enabled)
        assert change_status is True
        new_rests = tw.account.get_access_restrictions()
        assert current_rests.is_country_restrictions_enabled != new_rests.is_country_restrictions_enabled
        return_status = tw.account.turn_countries_restrictions(current_rests.is_country_restrictions_enabled)
        assert return_status is True
        prev_rests = tw.account.get_access_restrictions()
        assert prev_rests.is_country_restrictions_enabled == current_rests.is_country_restrictions_enabled

    def test_get_countries(self, tw: Timeweb):
        countries = tw.account.get_countries()
        assert isinstance(countries, schemas.AccessCountries)

    def test_add_allowed_country(self, tw: Timeweb):
        countries = tw.account.get_countries()
        assert 'CZ' in countries.countries.keys(), 'Czech not in array of countries!'
        add_status = tw.account.add_allowed_countries(['CZ'])
        assert add_status.countries[0].status == 'success'
        new_rests = tw.account.get_access_restrictions()
        assert 'CZ' in new_rests.white_list.countries
        remove_status = tw.account.remove_allowed_countries(['CZ'])
        assert remove_status.countries[0].status == 'success'

    def test_use_ip_restrictions(self, tw: Timeweb, my_ip: str):
        current_rests = tw.account.get_access_restrictions()
        add_status = tw.account.add_allowed_ips([my_ip])
        assert add_status.ips[0].status == 'success'
        enable_status = tw.account.turn_ips_restrictions(True)
        assert enable_status is True
        new_rests = tw.account.get_access_restrictions()
        assert new_rests.is_ip_restrictions_enabled == True
        disable_status = tw.account.turn_ips_restrictions(False)
        assert disable_status is True
        new2_rests = tw.account.get_access_restrictions()
        assert new2_rests.is_ip_restrictions_enabled == False
        remove_status = tw.account.remove_allowed_ips([my_ip])
        assert remove_status.ips[0].status == 'success'
        return_status = tw.account.turn_ips_restrictions(current_rests.is_ip_restrictions_enabled)
        assert return_status is True
        afterall_rests = tw.account.get_access_restrictions()
        assert current_rests.is_ip_restrictions_enabled == afterall_rests.is_ip_restrictions_enabled
