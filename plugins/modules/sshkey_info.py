#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016 Tomas Karasek <tom.to.the.k@gmail.com>
# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: sshkey_info
short_description: Gather information about Equinix Metal SSH keys
description:
    - Gather information about Equinix Metal SSH keys.
    - API is documented at U(https://metal.equinix.com/developers/api/sshkeys/).
version_added: '1.3.0'
author:
    - Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
  labels:
    description:
      - One or more ssh key labels.
    type: list
    elements: str
    aliases:
      - names
  ids:
    description:
      - One or more ssh key ids.
    type: list
    elements: str
  fingerprints:
    description:
      - One ore more ssh key fingerprints.
    type: list
    elements: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass the api token in module param api_token.

- name: Gather information about all ssh keys
  hosts: localhost
  tasks:
    - equinix.metal.sshkey_info:


- name: Gather information about a particular ssh key using ID
  hosts: localhost
  tasks:
    - equinix.metal.sshkey_info:
      ids:
        - 173d7f11-f7b9-433e-ac40-f1571a38037a
'''

RETURN = '''
sshkeys:
    description: Information about each ssh key that was found.
    type: list
    sample: [
        {
            "fingerprint": "5c:93:74:7c:ed:07:17:62:28:75:79:23:d6:08:93:46",
            "id": "41d61bd8-3342-428b-a09c-e67bdd18a9b7",
            "key": "ssh-dss AAAAB3NzaC1kc3MAAACBAIfNT5S0ncP4BBJBYNhNPxFF9lqVhfPeu6SM1LoCocxqDc1AT3zFRi8hjIf6TLZ2AA4FYbcAWxLMhiBxZRVldT9GdBXile78kAK5z3bKTwq152DCqpxwwbaTIggLFhsU8wrfBsPWnDuAxZ0h7mmrCjoLIE3CNLDA/NmV3iB8xMThAAAAFQCStcesSgR1adPORzBxTr7hug92LwAAAIBOProm3Gk+HWedLyE8IfofLaOeRnbBRHAOL4z0SexKkVOnQ/LGN/uDIIPGGBDYTvXgKZT+jbHeulRJ2jKgfSpGKN4JxFQ8uzVH492jEiiUJtT72Ss1dCV4PmyERVIw+f54itihV3z/t25dWgowhb0int8iC/OY3cGodlmYb3wdcQAAAIBuLbB45djZXzUkOTzzcRDIRfhaxo5WipbtEM2B1fuBt2gyrvksPpH/LK6xTjdIIb0CxPu4OCxwJG0aOz5kJoRnOWIXQGhH7VowrJhsqhIc8gN9ErbO5ea8b1L76MNcAotmBDeTUiPw01IJ8MdDxfmcsCslJKgoRKSmQpCwXQtN2g== tomk@hp2",
            "label": "mynewkey33"
        }
    ]
    returned: always
'''  # noqa

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, is_valid_uuid, serialize_sshkey


def get_sshkey_info(module):
    sshkeys = module.metal_conn.list_ssh_keys()

    if module.params.get('ids'):
        sshkeys = [s for s in sshkeys if s.id in module.params.get('ids')]
    elif module.params.get('labels'):
        sshkeys = [s for s in sshkeys if s.label in module.params.get('labels')]
    elif module.params.get('fingerprints'):
        sshkeys = [s for s in sshkeys if s.fingerprint in module.params.get('fingerprints')]

    return {
        'sshkeys': [serialize_sshkey(s) for s in sshkeys]
    }


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            ids=dict(type='list', elements='str'),
            labels=dict(type='list', elements='str', aliases=['names']),
            fingerprints=dict(type='list', elements='str'),
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ('labels', 'ids'),
            ('labels', 'fingerprints'),
            ('ids', 'fingerprints'),
        ]
    )

    try:
        module.exit_json(**get_sshkey_info(module))
    except Exception as e:
        module.fail_json(msg='failed to get sshkey info: %s' % to_native(e))


if __name__ == '__main__':
    main()
