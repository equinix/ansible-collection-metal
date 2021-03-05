#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016, Tomas Karasek <tom.to.the.k@gmail.com>
# (c) 2016, Matt Baldwin <baldwin@stackpointcloud.com>
# (c) 2016, Thibaud Morel l'Horset <teebes@gmail.com>
# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: device_info
short_description: Gather information about Equinix Metal devices
description:
    - Gather information about Equinix Metal devices.
    - API is documented at U(https://metal.equinix.com/developers/api/devices/).
version_added: 1.2.0
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
     - equinix.metal.metal_project
options:
    device_ids:
        description:
            - One or more device ids.
        type: list
        elements: str
    hostnames:
        description:
            - One or more hostnames.
        type: list
        elements: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all devices
  hosts: localhost
  tasks:
    - equinix.metal.device_info:


- name: Gather information about a particular device using ID
  hosts: localhost
  tasks:
    - equinix.metal.device_info:
      device_ids:
        - 173d7f11-f7b9-433e-ac40-f1571a38037a
'''

RETURN = '''
devices:
    description: Information about each device that was found
    type: list
    sample: '[{"hostname": "my-server.com", "id": "2a5122b9-c323-4d5c-b53c-9ad3f54273e7",
               "public_ipv4": "147.229.15.12", "private-ipv4": "10.0.15.12",
               "tags": [], "locked": false, "state": "provisioning",
               "public_ipv6": ""2604:1380:2:5200::3"}]'
    returned: always
'''


import traceback

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, serialize_device


def get_device_info(module):
    devices = module.get_devices()

    if module.params.get('device_ids'):
        devices = filter(lambda d: d.id in module.params.get('device_ids'), devices)
    elif module.params.get('hostnames'):
        devices = filter(lambda d: d.id in module.params.get('hostnames'), devices)

    return {
        'devices': [serialize_device(d) for d in devices]
    }


def main():
    module = AnsibleMetalModule(
        argument_spec=dict(
            device_ids=dict(type='list', elements='str'),
            hostnames=dict(type='list', elements='str'),
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ('hostnames', 'device_ids'),
        ]
    )

    try:
        module.exit_json(**get_device_info(module))
    except Exception as e:
        module.fail_json(msg='failed to get device info, error: %s' %
                         (to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
