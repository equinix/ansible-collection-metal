#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: plan_info
short_description: Gather information about Equinix Metal plans
description:
    - Gather information about Equinix Metal plans.
    - API is documented at U(https://metal.equinix.com/developers/api/plans/).
version_added: '1.4.0'
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
    names:
        description:
            - One or more plan names.
        type: list
        elements: str
    ids:
        description:
            - One or more plan ids.
        type: list
        elements: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all plans
  hosts: localhost
  tasks:
    - equinix.metal.plan_info:


- name: Gather information about a particular plan using ID
  hosts: localhost
  tasks:
    - equinix.metal.plan_info:
      ids:
        - 173d7f11-f7b9-433e-ac40-f1571a38037a
'''

RETURN = '''
plans:
    description: Information about each plan that was found
    type: list
    sample: '[{
                "id": "e69c0169-4726-46ea-98f1-939c9e8a3607",
                "name": "t1.small.x86",
                "description": "Our Type 0 configuration is a general use \"cloud killer\" server, with a Intel Atom 2.4Ghz processor and 8GB of RAM.",
                "available_in":[
                    "ams1",
                    "ewr1",
                    "sjc1",
                    "nrt1",
                ],
                "line": "baremetal",
                "pricing": {
                    "hour": 0.07
                },
                "slug": "baremetal_0",
                "specs": {
                    "cpus": [
                        {
                            "count": 1,
                            "type": "Intel Atom C2550 @ 2.4Ghz"
                        }
                    ],
                    "drives": [
                        {
                            "count": 1,
                            "size": "80GB",
                            "type": "SSD"
                        }
                    ],
                    "features": {
                        "raid": false,
                        "txt": true
                    },
                    "memory": {
                        "total": "8GB"
                    },
                    "nics": [
                        {
                            "count": 2,
                            "type": "1Gbps"
                        }
                    ]
                }
            }]'
    returned: always
'''

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, serialize_plan


def get_plan_info(module):
    plans = module.metal_conn.list_plans(params={'include': 'available_in'})

    if module.params.get('ids'):
        plans = [p for p in plans if p.id in module.params.get('ids')]
    elif module.params.get('names'):
        plans = [p for p in plans if p.name in module.params.get('names')]

    return {
        'plans': [serialize_plan(p) for p in plans]
    }


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            ids=dict(type='list', elements='str'),
            names=dict(type='list', elements='str'),
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ('names', 'ids'),
        ]
    )

    try:
        module.exit_json(**get_plan_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get plan info, error:  {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
