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


import time
import traceback

from ansible.module_utils._text import to_native

HAS_METAL_SDK = True
try:
    import packet
except ImportError:
    HAS_METAL_SDK = False

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, is_valid_hostname, is_valid_uuid
from ansible_collections.equinix.metal.plugins.module_utils.metal import serialize_device, get_devices, devices_with_ids, devices_with_hostnames

MAX_DEVICES = 100


def get_hostname_list(module):
    hostnames = [h.strip() for h in module.params.get('hostnames', [])]

    for hn in hostnames:
        if not is_valid_hostname(hn):
            raise Exception("Hostname '%s' does not seem to be valid" % hn)

    if len(hostnames) > MAX_DEVICES:
        raise Exception("You specified too many hostnames, max is %d" %
                        MAX_DEVICES)
    return hostnames


def get_device_id_list(module):
    device_ids = [di.strip() for di in module.params.get('device_ids', [])]

    for di in device_ids:
        if not is_valid_uuid(di):
            raise Exception("Device ID '%s' does not seem to be valid" % di)

    if len(device_ids) > MAX_DEVICES:
        raise Exception("You specified too many devices, max is %d" %
                        MAX_DEVICES)
    return device_ids


def get_device_info(module, metal_conn):
    project_id = module.params.get('project_id')
    devices = get_devices(metal_conn, project_id, MAX_DEVICES)

    if module.params.get('device_ids'):
        devices = devices_with_ids(devices, get_device_id_list(module))
    elif module.params.get('hostnames'):
        devices = devices_with_hostnames(devices, get_device_id_list(module))

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

    if not HAS_METAL_SDK:
        module.fail_json(msg='python-packet required for this module')

    metal_conn = packet.Manager(auth_token=module.params.get('api_token'))

    try:
        module.exit_json(**get_device_info(module, metal_conn))
    except Exception as e:
        module.fail_json(msg='failed to get device info, error: %s' %
                         (to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
