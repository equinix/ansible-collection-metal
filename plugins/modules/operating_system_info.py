#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: operating_system_info
short_description: Gather information about Equinix Metal operating_systems
description:
    - Gather information about Equinix Metal operating_systems.
    - API is documented at U(https://metal.equinix.com/developers/api/operating_systems/).
version_added: '1.4.0'
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
    slugs:
        description:
            - One or more operating_system slugs.
        type: list
        elements: str
    distros:
        description:
            - One or more operating_system distros.
        type: list
        elements: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all operating_systems
  hosts: localhost
  tasks:
    - equinix.metal.operating_system_info:


- name: Gather information about a particular operating_system using slug
  hosts: localhost
  tasks:
    - equinix.metal.operating_system_info:
      slugs:
        - ubuntu_20_10
'''

RETURN = '''
operating_systems:
    description: Information about each operating_system that was found
    type: list
    sample: '[{
                "distro": "ubuntu",
                "name": "Ubuntu 20.10",
                "provisionable_on": [
                    "c1.small.x86",
                    "baremetal_1",
                    "c2.medium.x86",
                    "c3.medium.x86",
                    "c3.small.x86",
                    "g2.large.x86",
                    "m1.xlarge.x86",
                    "baremetal_2",
                    "m2.xlarge.x86",
                    "m3.large.x86",
                    "n2.xlarge.x86",
                    "s1.large.x86",
                    "baremetal_s",
                    "s3.xlarge.x86",
                    "t1.small.x86",
                    "baremetal_0",
                    "x1.small.x86",
                    "baremetal_1e",
                    "x2.xlarge.x86",
                    "x3.xlarge.x86"
                ],
                "slug": "ubuntu_20_10",
                "version": "20.10"
            }]'
    returned: always
'''

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, serialize_operating_system


def get_operating_system_info(module):
    operating_systems = module.metal_conn.list_operating_systems(params={'include': 'available_in'})

    if module.params.get('slugs'):
        operating_systems = [o for o in operating_systems if o.slug in module.params.get('slugs')]
    elif module.params.get('distros'):
        operating_systems = [o for o in operating_systems if o.distro in module.params.get('distros')]

    return {
        'operating_systems': [serialize_operating_system(o) for o in operating_systems]
    }


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            slugs=dict(type='list', elements='str'),
            distros=dict(type='list', elements='str'),
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ('slugs', 'distros'),
        ]
    )

    try:
        module.exit_json(**get_operating_system_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get operating_system info, error:  {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
