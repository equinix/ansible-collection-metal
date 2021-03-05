#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nurfet Becirevic <nurfet.becirevic@gmail.com>
# Copyright: (c) 2017, Tomas Karasek <tom.to.the.k@gmail.com>
# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: ip_subnet
short_description: Assign IP subnet to a bare metal server.
description:
    - Assign or unassign IPv4 or IPv6 subnets to or from a device in Equinix Metal.
    - IPv4 subnets must come from already reserved block.
    - IPv6 subnets must come from publicly routable /56 block from your project.
    - See U(https://metal.equinix.com/developers/docs/networking/elastic-ips/) for more info on IP block reservation.
version_added: '1.4.0'
author:
    - Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
    - Nurfet Becirevic (@nurfet-becirevic) <nurfet.becirevic@gmail.com>
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
extends_documentation_fragment:
     - equinix.metal.metal
     - equinix.metal.metal_project_optional
options:
  hostname:
    description:
      - A hostname of a device to/from which to assign/remove a subnet.
    required: False
    type: str
  device_id:
    description:
      - UUID of a device to/from which to assign/remove a subnet.
    required: False
    type: str
  project_id:
    description:
      - UUID of a project of the device to/from which to assign/remove a subnet.
    type: str
  cidr:
    description:
      - IPv4 or IPv6 subnet which you want to manage. It must come from a reserved block for your project in the Packet Host.
    aliases: [name]
    type: str
    required: true
  state:
    description:
      - Desired state of the IP subnet on the specified device.
      - With state == C(present), you must specify either hostname or device_id. Subnet with given CIDR will then be assigned to the specified device.
      - With state == C(absent), you can specify either hostname or device_id. The subnet will be removed from specified devices.
      - If you leave both hostname and device_id empty, the subnet will be removed from any device it's assigned to.
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Create 1 device and assign an arbitrary public IPv4 subnet to it
  hosts: localhost
  tasks:

  - equinix.metal.device:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      hostnames: myserver
      operating_system: ubuntu_20_04
      plan: baremetal_0
      facility: sjc1
      state: active

# Pick an IPv4 address from a block allocated to your project.

  - equinix.metal.ip_subnet:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      hostname: myserver
      cidr: "147.75.201.78/32"

# Release IP address 147.75.201.78

- name: Unassign IP address from any device in your project
  hosts: localhost
  tasks:
  - equinix.metal.ip_subnet:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      cidr: "147.75.201.78/32"
      state: absent
'''

RETURN = '''
changed:
  description: True if an IP address assignments were altered in any way (created or removed).
  type: bool
  sample: True
  returned: success

device_id:
  type: str
  description: UUID of the device associated with the specified IP address.
  returned: success

subnet:
  description: Dict with data about the handled IP subnet.
  type: dict
  sample:
    address: 147.75.90.241
    address_family: 4
    assigned_to: { href : /devices/61f9aa5e-0530-47f5-97c2-113828e61ed0 }
    cidr: 31
    created_at: '2017-08-07T15:15:30Z'
    enabled: True
    gateway: 147.75.90.240
    href: /ips/31eda960-0a16-4c0f-b196-f3dc4928529f
    id: 1eda960-0a16-4c0f-b196-f3dc4928529f
    manageable: True
    management: True
    netmask: 255.255.255.254
    network: 147.75.90.240
    public: True
  returned: success
'''


from ansible.module_utils._text import to_native

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, is_valid_uuid, is_valid_hostname, serialize_ip


def parse_subnet_cidr(cidr):
    if "/" not in cidr:
        raise Exception("CIDR expression in wrong format, must be address/prefix_len")
    addr, prefixlen = cidr.split("/")
    try:
        prefixlen = int(prefixlen)
    except ValueError:
        raise("Wrong prefix length in CIDR expression {0}".format(cidr))
    return addr, prefixlen


def act_on_assignment(target_state, module):
    return_dict = {'changed': False}
    specified_cidr = module.params.get("cidr")
    address, prefixlen = parse_subnet_cidr(specified_cidr)

    device_id = None
    hostname = None

    if module.params.get('device_id'):
        device_id = module.params.get('device_id')
        if not is_valid_uuid(device_id):
            raise Exception("Device ID '{0}' does not seem to be valid".format(device_id))
    elif module.params.get('hostname'):
        hostname = module.params.get('hostname')
        if not is_valid_hostname(hostname):
            raise Exception("Hostname '{0}' does not seem to be valid".format(hostname))

    if module.check_mode:
        return return_dict

    if hostname is None and device_id is None:
        if target_state == 'absent':
            # The special case to release the IP from any assignment
            for d in module.get_devices():
                for ip in d.ip_addresses():
                    if ip['address'] == address and ip['cidr'] == prefixlen:
                        module.metal_conn.delete_ip(ip['id'])
                        return_dict['changed'] = True
                        return_dict['subnet'] = ip
                        return_dict['device_id'] = d.id
                        return return_dict
        raise Exception("If you assign an address, you must specify either "
                        "target device ID or target unique hostname.")

    if device_id is not None:
        device = module.metal_conn.get_device(device_id)
    else:
        all_devices = module.get_devices()
        matching_devices = [d for d in all_devices if d.hostname == hostname]
        if len(matching_devices) > 1:
            raise Exception("There are more than one devices matching given hostname {0}".format(hostname))
        if len(matching_devices) == 0:
            raise Exception("There is no device matching given hostname {0}".format(hostname))
        device = matching_devices[0]

    return_dict['device_id'] = device.id

    matching_ips = [i for i in device.ip_addresses if i['address'] == address and i['cidr'] == prefixlen]

    if len(matching_ips) > 1:
        raise Exception("IP address {0} is assigned more than once for device {1}".format(
                        specified_cidr, device.hostname))

    if len(matching_ips) == 1:
        return_dict['subnet'] = matching_ips[0]

    if target_state == "absent" and len(matching_ips) == 1:
        ip = matching_ips[0]
        module.metal_conn.delete_ip(ip['id'])
        return_dict['changed'] = True
        return return_dict

    if target_state == 'present' and len(matching_ips) == 0:
        ip = module.metal_conn.create_device_ip(device.id, specified_cidr)
        return_dict['subnet'] = serialize_ip(ip)
        return return_dict

    return return_dict


def main():
    module = AnsibleMetalModule(
        project_id_required=False,
        argument_spec=dict(
            device_id=dict(type='str'),
            hostname=dict(type='str'),
            cidr=dict(type='str', required=True, aliases=['name']),
            state=dict(choices=['present', 'absent'], default='present'),
        ),
        supports_check_mode=True,
        mutually_exclusive=[('hostname', 'device_id')],
        # TODO: sort this out, is project_id only sometimes needed?
        required_one_of=[['hostname', 'device_id', 'project_id']],
        required_by=dict(
            hostname=('project_id',),
        ),
    )

    state = module.params.get('state')

    try:
        module.exit_json(**act_on_assignment(state, module))
    except Exception as e:
        module.fail_json(
            msg="failed to set IP subnet to state {0}, error: {1}".format(state, to_native(e)))


if __name__ == '__main__':
    main()
