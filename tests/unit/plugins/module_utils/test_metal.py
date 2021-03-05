# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import os
import unittest

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, is_valid_hostname


@pytest.mark.parametrize('stdin', [{}], indirect=['stdin'])
def test_get_api_token_param_not_specified(stdin, capsys):
    with pytest.raises(SystemExit) as e:
        AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert e.type == SystemExit

    out, _ = capsys.readouterr()  # pylint: disable=blacklisted-name
    assert "missing required arguments: api_token" in out


@pytest.mark.parametrize('stdin', [{'api_token': 'deadbeef'}], indirect=['stdin'])
def test_get_api_token_param_from_stdin(stdin):
    module = AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert module.params.get('api_token') == 'deadbeef'


@pytest.mark.parametrize('stdin', [{'auth_token': 'deadbeef'}], indirect=['stdin'])
def test_get_api_token_param_from_stdin_fallback(stdin):
    module = AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert module.params.get('api_token') == 'deadbeef'


@pytest.mark.parametrize('stdin', [{}], indirect=['stdin'])
def test_get_api_token_param_from_env(stdin):
    os.environ['METAL_API_TOKEN'] = 'deadbeef'
    module = AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert module.params.get('api_token') == 'deadbeef'


@pytest.mark.parametrize('stdin', [{}], indirect=['stdin'])
def test_get_api_token_param_from_env_fallback(stdin):
    os.environ['PACKET_API_TOKEN'] = 'deadbeef'
    module = AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert module.params.get('api_token') == 'deadbeef'


@pytest.mark.parametrize('stdin', [{}], indirect=['stdin'])
def test_get_api_token_param_from_env_fallback_more(stdin):
    os.environ['PACKET_TOKEN'] = 'deadbeef'
    module = AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert module.params.get('api_token') == 'deadbeef'


@pytest.mark.parametrize('stdin', [{'api_token': 'deadbeef'}], indirect=['stdin'])
def test_get_api_token_param_stdin_pref(stdin):
    os.environ['PACKET_TOKEN'] = 'donotwant'
    module = AnsibleMetalModule(argument_spec=dict(), project_id_arg=False)
    assert module.params.get('api_token') == 'deadbeef'


class TestIsValidHostname(unittest.TestCase):

    def test_valid_hostname(self):
        self.assertTrue(is_valid_hostname("good-hostname"))

    def test_leading_dash(self):
        self.assertFalse(is_valid_hostname("-hostname"))

    def test_underscores(self):
        self.assertFalse(is_valid_hostname("bad_hostname"))
