#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: user_info
short_description: Gather information about the logged in user
description:
    - Gather information about the logged in user for Equinix Metal.
    - See U(https://metal.equinix.com/developers/api/users/#retrieve-the-current-user) for more info on users.
version_added: '1.4.0'
author:
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about the current logged in user
  hosts: localhost
  tasks:
    - equinix.metal.user_info:
'''

RETURN = '''
user:
    description: Information about the logged in user.
    type: dict
    sample: '{
        "avatar_thumb_url": "https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm",
        "avatar_url": "https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm",
        "created_at": "2021-02-26T14:08:17Z",
        "customdata": {},
        "default_organization_id": "594b06f3-cef2-4127-85fd-08332fcf0021",
        "default_project_id": null,
        "email": "does@not.exist",
        "emails": [
            {
                "href": "/emails/7c281a6b-1801-4008-89f3-0a43a2fb26e1"
            }
        ],
        "features": [
            "maintenance_mail",
            "deploy_without_public_ip",
            "advanced_ips",
            "block_storage",
            "bgp_default_route",
            "native_vlan",
        ],
        "first_name": "Does",
        "full_name": "Does Not Exist",
        "href": "/users/7867d973-9b75-48dc-b94f-0d0a87e9dda0",
        "id": "7867d973-9b75-48dc-b94f-0d0a87e9dda0",
        "language": null,
        "last_login_at": "2021-03-02T21:48:07Z",
        "last_name": "Not Exist",
        "mailing_address": null,
        "max_projects": 0,
        "number_of_ssh_keys": 0,
        "opt_in": false,
        "opt_in_updated_at": null,
        "phone_number": null,
        "restricted": false,
        "short_id": "7867d973",
        "social_accounts": {},
        "timezone": "America/New_York",
        "two_factor_auth": "",
        "updated_at": "2021-03-02T08:23:18Z",
        "verification_stage": "verified",
        "vpn": false
    }'
    returned: always
'''


from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule


def get_user_info(module):
    user = module.metal_conn.get_user()
    return {
        'user': user
    }


def main():
    module = AnsibleMetalModule(
        argument_spec=dict(),
        supports_check_mode=True,
        project_id_arg=False,
    )

    try:
        module.exit_json(**get_user_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get user info, error: {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
