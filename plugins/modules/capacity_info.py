#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: capacity_info
short_description: Gather information about Equinix Metal capacity
description:
    - Gather information about Equinix Metal capacity.
    - API is documented at U(https://metal.equinix.com/developers/api/capacity/).
version_added: '1.4.0'
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
    include_legacy:
        description:
            - Include legacy facilities.
        type: bool
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all capacity
  hosts: localhost
  tasks:
    - equinix.metal.capacity_info:
'''

RETURN = '''
capacity:
    description: Information about capacity that was found
    type: dict
    sample: '{
                "da11": {
                    "c3.medium.x86": {
                        "level": "normal"
                    },
                    "c3.small.x86": {
                        "level": "normal"
                    },
                    "m3.large.x86": {
                        "level": "normal"
                    },
                    "n2.xlarge.x86": {
                        "level": "unavailable"
                    },
                    "s3.xlarge.x86": {
                        "level": "normal"
                    }
                },
            }'
    returned: always
'''

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule


def get_capacity_info(module):
    include_legacy = module.params.get('include_legacy')
    legacy = 'include' if include_legacy else 'exclude'
    capacity = module.metal_conn.get_capacity(legacy=legacy)

    return capacity


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            include_legacy=dict(type='bool'),
        ),
        supports_check_mode=True,
    )

    try:
        module.exit_json(**get_capacity_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get capacity info, error:  {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
