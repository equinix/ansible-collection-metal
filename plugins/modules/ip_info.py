#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: ip_info
short_description: Gather information about project IP Addresses
description:
    - Gather information about project IP addresses in Equinix Metal.
    - See U(https://metal.equinix.com/developers/api/ipaddresses/) for more info on IP Addresses.
version_added: '1.4.0'
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
     - equinix.metal.metal_project
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all devices
  hosts: localhost
  tasks:
    - equinix.metal.ip_info:
        project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
'''

RETURN = '''
ips:
    description: Information about each ip address that was found
    type: list
    sample: '[{"address": "136.144.57.174",
               "address_family": 4,
               "assigned_to": null,
               "cidr": 32,
               "created_at": "2021-01-05T18:55:55Z",
               "customdata": {},
               "details": null,
               "enabled": true,
               "facility": "dc13",
               "gateway": "136.144.57.174",
               "global_ip": false,
               "id": "d6764db0-69c6-44e9-922e-18146608cd3a",
               "interface": null,
               "management": false,
               "netmask": "255.255.255.255",
               "network": "136.144.57.174",
               "project_id": "f2a2d7ad-886e-4207-bf38-10ebdf49cf84",
               "public": true,
               "tags": ["cluster-api-provider-packet:cluster-id:versiontest"]}]'
    returned: always
'''


from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, is_valid_uuid, serialize_ip


def get_ip_info(module):
    project_id = module.params.get('project_id')
    if not is_valid_uuid(project_id):
        raise Exception("Project ID {0} does not seem to be valid".format(project_id))

    ips = module.metal_conn.list_project_ips(project_id)
    return {
        'ips': [serialize_ip(i) for i in ips]
    }


def main():
    module = AnsibleMetalModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        module.exit_json(**get_ip_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get project IP info, error: {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
