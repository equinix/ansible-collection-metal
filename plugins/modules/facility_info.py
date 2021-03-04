#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: facility_info
short_description: Gather information about Equinix Metal facilities
description:
    - Gather information about Equinix Metal facilities.
    - API is documented at U(https://metal.equinix.com/developers/api/facilities/).
version_added: '1.4.0'
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
    codes:
        description:
            - One or more facility codes.
        type: list
        elements: str
    ids:
        description:
            - One or more facility ids.
        type: list
        elements: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all facilities
  hosts: localhost
  tasks:
    - equinix.metal.facility_info:


- name: Gather information about a particular facility using ID
  hosts: localhost
  tasks:
    - equinix.metal.facility_info:
      ids:
        - 173d7f11-f7b9-433e-ac40-f1571a38037a
'''

RETURN = '''
facilities:
    description: Information about each facility that was found
    type: list
    sample: '[{
                'id': '8e6470b3-b75e-47d1-bb93-45b225750975',
                'name': 'Amsterdam, NL',
                'code': 'ams1',
                'features': [
                    'baremetal',
                    'storage',
                    'global_ipv4',
                    'backend_transfer',
                    'layer_2'
                ],
                'address': {
                    'href': '#0688e909-647e-4b21-bdf2-fc056d993fc5'
                }
            }]'
    returned: always
'''

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, serialize_facility


def get_facility_info(module):
    facilities = module.metal_conn.list_facilities()

    if module.params.get('ids'):
        facilities = [f for f in facilities if f.id in module.params.get('ids')]
    elif module.params.get('codes'):
        facilities = [f for f in facilities if f.code in module.params.get('codes')]

    return {
        'facilities': [serialize_facility(f) for f in facilities]
    }


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            ids=dict(type='list', elements='str'),
            codes=dict(type='list', elements='str'),
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ('codes', 'ids'),
        ]
    )

    try:
        module.exit_json(**get_facility_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get facility info, error:  {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
