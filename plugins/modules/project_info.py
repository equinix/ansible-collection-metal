#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nurfet Becirevic <nurfet.becirevic@gmail.com>
# Copyright: (c) 2019, Tomas Karasek <tom.to.the.k@gmail.com>
# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: project_info
short_description: Gather information about Equinix Metal projects
description:
    - Gather information about Equinix Metal projects.
    - API is documented at U(https://metal.equinix.com/developers/api/projects/).
version_added: '1.2.0'
author:
    - Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
    - Nurfet Becirevic (@nurfet-becirevic) <nurfet.becirevic@gmail.com>
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
options:
    names:
        description:
            - One or more project names.
        type: list
        elements: str
    ids:
        description:
            - One or more project ids.
        type: list
        elements: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all projects
  hosts: localhost
  tasks:
    - equinix.metal.project_info:


- name: Gather information about a particular project using ID
  hosts: localhost
  tasks:
    - equinix.metal.project_info:
      ids:
        - 173d7f11-f7b9-433e-ac40-f1571a38037a
'''

RETURN = '''
projects:
    description: Information about each project that was found
    type: list
    sample: '[{"name": "my-project", "id": "2a5122b9-c323-4d5c-b53c-9ad3f54273e7"}]'
    returned: always
'''

from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, serialize_project


def get_project_info(module):
    projects = module.metal_conn.list_projects()

    if module.params.get('ids'):
        projects = [p for p in projects if p.id in module.params.get('ids')]
    elif module.params.get('names'):
        projects = [p for p in projects if p.name in module.params.get('names')]

    return {
        'projects': [serialize_project(p) for p in projects]
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
        module.exit_json(**get_project_info(module))
    except Exception as e:
        module.fail_json(
            msg="failed to get project info, error:  {0}".format(to_native(e)))


if __name__ == '__main__':
    main()
