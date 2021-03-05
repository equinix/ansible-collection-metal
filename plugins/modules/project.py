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
module: project
short_description: Create/delete a project in Equinix Metal
description:
    - Create/delete a project in Equinix Metal.
    - API is documented at U(https://metal.equinix.com/developers/api/projects/).
version_added: '1.2.0'
author:
    - Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
    - Nurfet Becirevic (@nurfet-becirevic) <nurfet.becirevic@gmail.com>
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
  payment_method:
    description:
      - Payment method is name of one of the payment methods available to your user.
      - When blank, the API assumes the default payment method.
    type: str
  name:
     description:
       - Name for/of the project.
     type: str
  org_id:
    description:
      - UUID of the organization to create a project for.
      - When blank, the API assumes the default organization.
    type: str
  id:
    description:
      - UUID of the project which you want to remove.
    type: str
  custom_data:
    description:
      - Custom data about the project to create.
    type: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass the api token in module param api_token.

- name: Create new project
  hosts: localhost
  tasks:
    equinix.metal.project:
      name: "new project"

- name: Create new project within non-default organization
  hosts: localhost
  tasks:
    equinix.metal.project:
      name: "my org project"
      org_id: a4cc87f9-e00f-48c2-9460-74aa60beb6b0

- name: Remove project by id
  hosts: localhost
  tasks:
    equinix.metal.project:
      state: absent
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6

- name: Create new project with non-default billing method
  hosts: localhost
  tasks:
    equinix.metal.project:
      name: "newer project"
      payment_method: "the other visa"
'''

RETURN = '''
changed:
  description: True if a project was created or removed.
  type: bool
  sample: True
  returned: success

name:
  description: Name of addressed project.
  type: str
  returned: success

id:
  description: UUID of addressed project.
  type: str
  returned: success
'''

from ansible.module_utils._text import to_native

HAS_METAL_SDK = True
try:
    import packet
except ImportError:
    HAS_METAL_SDK = False

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule


def act_on_project(target_state, module):
    result_dict = {'changed': False}
    given_id = module.params.get('id')
    given_name = module.params.get('name')
    if given_id:
        matching_projects = [
            p for p in module.metal_conn.list_projects() if given_id == p.id]
    else:
        matching_projects = [
            p for p in module.metal_conn.list_projects() if given_name == p.name]

    if target_state == 'present':
        if len(matching_projects) == 0:
            org_id = module.params.get('org_id')
            custom_data = module.params.get('custom_data')
            payment_method = module.params.get('payment_method')

            if not org_id:
                params = {
                    "name": given_name,
                    "payment_method_id": payment_method,
                    "customdata": custom_data
                }
                new_project_data = module.metal_conn.call_api("projects", "POST", params)
                new_project = packet.Project(new_project_data, module.metal_conn)
            else:
                new_project = module.metal_conn.create_organization_project(
                    org_id=org_id,
                    name=given_name,
                    payment_method_id=payment_method,
                    customdata=custom_data
                )

            result_dict['changed'] = True
            matching_projects.append(new_project)

        result_dict['name'] = matching_projects[0].name
        result_dict['id'] = matching_projects[0].id
    else:
        if len(matching_projects) > 1:
            _msg = ("More than projects matched for module call with state = absent: "
                    "{0}".format(to_native(matching_projects)))
            module.fail_json(msg=_msg)

        if len(matching_projects) == 1:
            p = matching_projects[0]
            result_dict['name'] = p.name
            result_dict['id'] = p.id
            result_dict['changed'] = True
            try:
                p.delete()
            except Exception as e:
                _msg = ("while trying to remove project {0}, id {1}, got error: {2}".format(
                        p.name, p.id, to_native(e)))
                module.fail_json(msg=_msg)
    return result_dict


def main():
    module = AnsibleMetalModule(
        project_id_arg=False,
        argument_spec=dict(
            state=dict(choices=['present', 'absent'], default='present'),
            name=dict(type='str'),
            id=dict(type='str'),
            org_id=dict(type='str'),
            payment_method=dict(type='str'),
            custom_data=dict(type='str'),
        ),
        supports_check_mode=True,
        required_one_of=[("name", "id",)],
        mutually_exclusive=[
            ('name', 'id'),
        ]
    )
    if not HAS_METAL_SDK:
        module.fail_json(msg='python-packet required for this module')

    state = module.params.get('state')

    # TODO: implement proper check mode
    if module.check_mode:
        module.exit_json(changed=False)

    try:
        module.exit_json(**act_on_project(state, module))
    except Exception as e:
        module.fail_json(
            msg="failed to set project state {0}: {1}".format(state, to_native(e)))


if __name__ == '__main__':
    main()
