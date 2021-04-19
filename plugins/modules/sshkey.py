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
module: sshkey
short_description: Create/delete an SSH key in Equinix Metal
description:
    - Create/delete an SSH key in Equinix Metal.
    - API is documented at U(https://metal.equinix.com/developers/api/sshkeys/).
version_added: '1.3.0'
author:
    - Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
  state:
    description:
      - Indicate desired state of the target.
    default: present
    choices: ['present', 'absent']
    type: str
  label:
    description:
      - Label for the key. If you keep it empty, it will be read from key string.
    type: str
    aliases:
      - name
  id:
    description:
      - UUID of the key which you want to remove.
    type: str
  fingerprint:
    description:
      - Fingerprint of the key which you want to remove.
    type: str
  key:
    description:
      - Public Key string ({type} {base64 encoded key} {description}).
    type: str
  key_file:
    description:
      - File with the public key.
    type: path
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass the api token in module param api_token.

- name: Create sshkey from string
  hosts: localhost
  tasks:
    equinix.metal.sshkey:
      key: "{{ lookup('ansible.builtin.file', 'my_sshkey.pub') }}"

- name: Create sshkey from file
  hosts: localhost
  tasks:
    equinix.metal.sshkey:
      label: key from file
      key_file: ~/ff.pub

- name: Remove sshkey by id
  hosts: localhost
  tasks:
    equinix.metal.sshkey:
      state: absent
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
'''

RETURN = '''
changed:
    description: True if a sshkey was created or removed.
    type: bool
    sample: True
    returned: always
sshkeys:
    description: Information about sshkeys that were created/removed.
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


def load_key_string(key_str):
    ret_dict = {}
    key_str = key_str.strip()
    ret_dict['key'] = key_str
    cut_key = key_str.split()
    if len(cut_key) in [2, 3]:
        if len(cut_key) == 3:
            ret_dict['label'] = cut_key[2]
    else:
        raise Exception("Public key %s is in wrong format" % key_str)
    return ret_dict


def get_sshkey_selector(module):
    key_id = module.params.get('id')
    if key_id:
        if not is_valid_uuid(key_id):
            raise Exception("sshkey ID %s is not valid UUID" % key_id)
    selecting_fields = ['label', 'fingerprint', 'id', 'key']
    select_dict = {}
    for f in selecting_fields:
        if module.params.get(f) is not None:
            select_dict[f] = module.params.get(f)

    if module.params.get('key_file'):
        with open(module.params.get('key_file')) as _file:
            loaded_key = load_key_string(_file.read())
        select_dict['key'] = loaded_key['key']
        if module.params.get('label') is None:
            if loaded_key.get('label'):
                select_dict['label'] = loaded_key['label']

    def selector(k):
        if 'key' in select_dict:
            # if key string is specified, compare only the key strings
            return k.key == select_dict['key']
        else:
            # if key string not specified, all the fields must match
            return all([select_dict[f] == getattr(k, f) for f in select_dict])
    return selector


def act_on_sshkeys(target_state, module):
    selector = get_sshkey_selector(module)
    existing_sshkeys = module.metal_conn.list_ssh_keys()
    matching_sshkeys = list(filter(selector, existing_sshkeys))
    changed = False
    if target_state == 'present':
        if matching_sshkeys == []:
            # there is no key matching the fields from module call
            # => create the key, label and
            newkey = {}
            if module.params.get('key_file'):
                with open(module.params.get('key_file')) as f:
                    newkey = load_key_string(f.read())
            if module.params.get('key'):
                newkey = load_key_string(module.params.get('key'))
            if module.params.get('label'):
                newkey['label'] = module.params.get('label')
            for param in ('label', 'key'):
                if param not in newkey:
                    _msg = ("If you want to ensure a key is present, you must "
                            "supply both a label and a key string, either in "
                            "module params, or in a key file. %s is missing"
                            % param)
                    raise Exception(_msg)
            matching_sshkeys = []
            new_key_response = module.metal_conn.create_ssh_key(
                newkey['label'], newkey['key'])
            changed = True

            matching_sshkeys.append(new_key_response)
    else:
        # state is 'absent' => delete matching keys
        for k in matching_sshkeys:
            try:
                k.delete()
                changed = True
            except Exception as e:
                _msg = ("while trying to remove sshkey %s, id %s %s, "
                        "got error: %s" %
                        (k.label, k.id, target_state, e))
                raise Exception(_msg)

    return {
        'changed': changed,
        'sshkeys': [serialize_sshkey(k) for k in matching_sshkeys]
    }


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            state=dict(choices=['present', 'absent'], default='present'),
            label=dict(type='str', aliases=['name'], default=None),
            id=dict(type='str', default=None),
            fingerprint=dict(type='str', default=None),
            key=dict(type='str', default=None, no_log=True),
            key_file=dict(type='path', default=None),
        ),
        mutually_exclusive=[
            ('label', 'id'),
            ('label', 'fingerprint'),
            ('id', 'fingerprint'),
            ('key', 'fingerprint'),
            ('key', 'id'),
            ('key_file', 'key'),
        ]
    )

    state = module.params.get('state')

    try:
        module.exit_json(**act_on_sshkeys(state, module))
    except Exception as e:
        module.fail_json(msg='failed to set sshkey state: %s' % to_native(e))


if __name__ == '__main__':
    main()
