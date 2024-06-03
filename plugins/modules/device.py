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
module: device
short_description: Manage a bare metal server in Equinix Metal
description:
    - Manage a bare metal server in Equinix Metal (a "device" in the API terms).
    - When the machine is created it can optionally wait for public IP address, or for active state.
    - API is documented at U(https://metal.equinix.com/developers/api/devices/).
version_added: 1.1.0
author:
    - Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
    - Matt Baldwin (@baldwinSPC) <baldwin@stackpointcloud.com>
    - Thibaud Morel l'Horset (@teebes) <teebes@gmail.com>
    - Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
notes:
     - Doesn't support check mode.
extends_documentation_fragment:
     - equinix.metal.metal
     - equinix.metal.metal_project
options:
    count:
        description:
            - The number of devices to create. Count number can be included in hostname via the %d string formatter.
        default: 1
        type: int
    count_offset:
        description:
            - From which number to start the count.
        default: 1
        type: int
    device_ids:
        description:
            - List of device IDs on which to operate.
        type: list
        elements: str
    tags:
        description:
            - List of device tags.
            - Currently implemented only for device creation.
        type: list
        elements: str
    facility:
        description:
            - Facility slug for device creation. See the Equinix Metal API for current list - U(https://metal.equinix.com/developers/api/facilities/).
        type: str
    features:
        description:
            - Dict with "features" for device creation. See Equinix Metal API docs for details.
        type: dict
    hostnames:
        description:
            - A hostname of a device, or a list of hostnames.
            - If given string or one-item list, you can use the C("%d") Python string format to expand numbers from I(count).
            - If only one hostname, it might be expanded to list if I(count)>1.
        aliases: [name]
        type: list
        elements: str
    locked:
        description:
            - Whether to lock a created device.
        default: false
        aliases: [lock]
        type: bool
    operating_system:
        description:
            - OS slug for device creation. See Equinix Metal API for current list - U(https://metal.equinix.com/developers/api/operatingsystems/).
        type: str
    plan:
        description:
            - Plan slug for device creation. See Equinix Metal API for current list - U(https://metal.equinix.com/developers/api/plans/).
        type: str
    state:
        description:
            - Desired state of the device.
            - If set to C(present) (the default), the module call will return immediately after the device-creating HTTP request successfully returns.
            - If set to C(active), the module call will block until all the specified devices are in state active, or until I(wait_timeout).
        choices: [present, absent, active, inactive, rebooted]
        default: present
        type: str
    user_data:
        description:
            - Userdata blob made available to the machine.
        type: str
    wait_for_public_IPv:
        description:
            - Whether to wait for the instance to be assigned a public IPv4/IPv6 address.
            - If set to 4, it will wait until IPv4 is assigned to the instance.
            - If set to 6, wait until public IPv6 is assigned to the instance.
        choices: [4,6]
        type: int
    wait_timeout:
        description:
            - How long (seconds) to wait either for automatic IP address assignment, or for the device to reach the C(active) I(state).
            - If I(wait_for_public_IPv) is set and I(state) is C(active), the module will wait for both events consequently, applying the timeout twice.
        default: 900
        type: int
    ipxe_script_url:
        description:
            - URL of custom iPXE script for provisioning.
            - More about custom iPXE for Equinix Metal devices at U(https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/).
        type: str
    always_pxe:
        description:
            - Persist PXE as the first boot option.
            - Normally, the PXE process happens only on the first boot. Set this arg to have your device continuously boot to iPXE.
        default: false
        type: bool
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

# Creating devices

- name: Create 1 device
  hosts: localhost
  tasks:
  - equinix.metal.device:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      hostnames: myserver
      tags: ci-xyz
      operating_system: ubuntu_16_04
      plan: baremetal_0
      facility: sjc1

# Create the same device and wait until it is in state "active", (when it's
# ready for other API operations). Fail if the device is not "active" in
# 10 minutes.

- name: Create device and wait up to 10 minutes for active state
  hosts: localhost
  tasks:
  - equinix.metal.device:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      hostnames: myserver
      operating_system: ubuntu_16_04
      plan: baremetal_0
      facility: sjc1
      state: active
      wait_timeout: 600

- name: Create 3 ubuntu devices called server-01, server-02 and server-03
  hosts: localhost
  tasks:
  - equinix.metal.device:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      hostnames: server-%02d
      count: 3
      operating_system: ubuntu_16_04
      plan: baremetal_0
      facility: sjc1

- name: Create 3 coreos devices with userdata, wait until they get IPs and then wait for SSH
  hosts: localhost
  tasks:
  - name: Create 3 devices and register their facts
    equinix.metal.device:
      hostnames: [coreos-one, coreos-two, coreos-three]
      operating_system: coreos_stable
      plan: baremetal_0
      facility: ewr1
      locked: true
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      wait_for_public_IPv: 4
      user_data: |
        #cloud-config
        ssh_authorized_keys:
          - {{ lookup('ansible.builtin.file', 'my_equinix_metal_sshkey') }}
        coreos:
          etcd:
            discovery: https://discovery.etcd.io/6a28e078895c5ec737174db2419bb2f3
            addr: $private_ipv4:4001
            peer-addr: $private_ipv4:7001
          fleet:
            public-ip: $private_ipv4
          units:
            - name: etcd.service
              command: start
            - name: fleet.service
              command: start
    register: newhosts

  - name: Wait for ssh
    ansible.builtin.wait_for:
      delay: 1
      host: "{{ item.public_ipv4 }}"
      port: 22
      state: started
      timeout: 500
    with_items: "{{ newhosts.devices }}"


# Other states of devices

- name: Remove 3 devices by uuid
  hosts: localhost
  tasks:
  - equinix.metal.device:
      project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
      state: absent
      device_ids:
        - 1fb4faf8-a638-4ac7-8f47-86fe514c30d8
        - 2eb4faf8-a638-4ac7-8f47-86fe514c3043
        - 6bb4faf8-a638-4ac7-8f47-86fe514c301f
'''

RETURN = '''
changed:
    description: True if a device was altered in any way (created, modified or removed)
    type: bool
    sample: True
    returned: success

devices:
    description: Information about each device that was processed
    type: list
    sample: '[{"hostname": "my-server.com", "id": "2a5122b9-c323-4d5c-b53c-9ad3f54273e7",
               "public_ipv4": "147.229.15.12", "private-ipv4": "10.0.15.12",
               "tags": [], "locked": false, "state": "provisioning",
               "public_ipv6": ""2604:1380:2:5200::3"}]'
    returned: success
'''  # NOQA


import re
import time
import traceback

from ansible.module_utils._text import to_native

HAS_METAL_SDK = True
try:
    import packet
except ImportError:
    HAS_METAL_SDK = False

from ansible_collections.equinix.metal.plugins.module_utils.metal import AnsibleMetalModule, is_valid_uuid, is_valid_hostname, serialize_device

METAL_DEVICE_STATES = (
    'queued',
    'provisioning',
    'failed',
    'powering_on',
    'active',
    'powering_off',
    'inactive',
    'rebooting',
)


ALLOWED_STATES = ['absent', 'active', 'inactive', 'rebooted', 'present']


def get_hostname_list(module):
    hostnames = module.params.get('hostnames')
    count = module.params.get('count')
    count_offset = module.params.get('count_offset')

    if (len(hostnames) > 1) and (count > 1):
        _msg = ("If you set count>1, you should only specify one hostname "
                "with the %d formatter, not a list of hostnames.")
        raise Exception(_msg)

    if (len(hostnames) == 1) and (count > 0):
        hostname_spec = hostnames[0]
        count_range = range(count_offset, count_offset + count)
        if re.search(r"%\d{0,2}d", hostname_spec):
            hostnames = [hostname_spec % i for i in count_range]
        elif count > 1:
            hostname_spec = '%s%%02d' % hostname_spec
            hostnames = [hostname_spec % i for i in count_range]

    for hn in hostnames:
        if not is_valid_hostname(hn):
            raise Exception("Hostname '%s' does not seem to be valid" % hn)

    return hostnames


def get_device_id_list(module):
    device_ids = module.params.get('device_ids')

    for di in device_ids:
        if not is_valid_uuid(di):
            raise Exception("Device ID '%s' does not seem to be valid" % di)

    return device_ids


def create_single_device(module, hostname):

    for param in ('hostnames', 'operating_system', 'plan'):
        if not module.params.get(param):
            raise Exception("%s parameter is required for new device."
                            % param)
    project_id = module.params.get('project_id')
    plan = module.params.get('plan')
    tags = module.params.get('tags')
    user_data = module.params.get('user_data')
    facility = module.params.get('facility')
    operating_system = module.params.get('operating_system')
    locked = module.params.get('locked')
    ipxe_script_url = module.params.get('ipxe_script_url')
    always_pxe = module.params.get('always_pxe')
    if operating_system != 'custom_ipxe':
        for param in ('ipxe_script_url', 'always_pxe'):
            if module.params.get(param):
                raise Exception('%s parameter is not valid for non custom_ipxe operating_system.' % param)

    device = module.metal_conn.create_device(
        project_id=project_id,
        hostname=hostname,
        tags=tags,
        plan=plan,
        facility=facility,
        operating_system=operating_system,
        userdata=user_data,
        locked=locked,
        ipxe_script_url=ipxe_script_url,
        always_pxe=always_pxe)
    return device


def refresh_device_list(module, devices):
    device_ids = [d.id for d in devices]
    new_device_list = module.get_devices()
    return [d for d in new_device_list if d.id in device_ids]


def wait_for_devices_active(module, watched_devices):
    wait_timeout = module.params.get('wait_timeout')
    wait_timeout = time.time() + wait_timeout
    refreshed = watched_devices
    while wait_timeout > time.time():
        refreshed = refresh_device_list(module, watched_devices)
        if len(refreshed) == len(watched_devices) and all(d.state == 'active' for d in refreshed):
            return refreshed
        time.sleep(5)
    raise Exception("Waiting for state \"active\" timed out for devices: %s"
                    % [d.hostname for d in refreshed if d.state != "active"])


def wait_for_public_IPv(module, created_devices):

    def has_public_ip(addr_list, ip_v):
        return any([a['public'] and a['address_family'] == ip_v
                    and a['address'] for a in addr_list])

    def all_have_public_ip(ds, ip_v):
        return all([has_public_ip(d.ip_addresses, ip_v) for d in ds])

    address_family = module.params.get('wait_for_public_IPv')

    wait_timeout = module.params.get('wait_timeout')
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        refreshed = refresh_device_list(module, created_devices)
        if len(refreshed) == len(created_devices) and all_have_public_ip(refreshed, address_family):
            return refreshed
        time.sleep(5)

    raise Exception("Waiting for IPv%d address timed out. Hostnames: %s"
                    % (address_family, [d.hostname for d in created_devices]))


def get_specified_device_identifiers(module):
    if module.params.get('device_ids'):
        device_id_list = get_device_id_list(module)
        return {'ids': device_id_list, 'hostnames': []}
    elif module.params.get('hostnames'):
        hostname_list = get_hostname_list(module)
        return {'hostnames': hostname_list, 'ids': []}


def act_on_devices(module, target_state):
    specified_identifiers = get_specified_device_identifiers(module)
    existing_devices = module.get_devices()
    changed = False
    create_hostnames = []
    if target_state in ['present', 'active', 'rebooted']:
        # states where we might create non-existing specified devices
        existing_devices_names = [ed.hostname for ed in existing_devices]
        create_hostnames = [hn for hn in specified_identifiers['hostnames']
                            if hn not in existing_devices_names]

    process_devices = [d for d in existing_devices
                       if (d.id in specified_identifiers['ids'])
                       or (d.hostname in specified_identifiers['hostnames'])]

    if target_state != 'present':
        _absent_state_map = {}
        for s in METAL_DEVICE_STATES:
            _absent_state_map[s] = packet.Device.delete

        state_map = {
            'absent': _absent_state_map,
            'active': {'inactive': packet.Device.power_on,
                       'provisioning': None, 'rebooting': None
                       },
            'inactive': {'active': packet.Device.power_off},
            'rebooted': {'active': packet.Device.reboot,
                         'inactive': packet.Device.power_on,
                         'provisioning': None, 'rebooting': None
                         },
        }

        # First do non-creation actions, it might be faster
        for d in process_devices:
            if d.state == target_state:
                continue
            if d.state in state_map[target_state]:
                api_operation = state_map[target_state].get(d.state)
                if api_operation is not None:
                    api_operation(d)
                    # TODO: update device status after operation
                    changed = True
            else:
                _msg = (
                    "I don't know how to process existing device %s from state %s "
                    "to state %s" %
                    (d.hostname, d.state, target_state))
                raise Exception(_msg)

    # At last create missing devices
    created_devices = []
    if create_hostnames:
        created_devices = [create_single_device(module, n)
                           for n in create_hostnames]
        if module.params.get('wait_for_public_IPv'):
            created_devices = wait_for_public_IPv(
                module, created_devices)
        changed = True

    processed_devices = created_devices + process_devices
    if target_state == 'active':
        processed_devices = wait_for_devices_active(
            module, processed_devices)

    return {
        'changed': changed,
        'devices': [serialize_device(d) for d in processed_devices]
    }


def main():
    module = AnsibleMetalModule(
        argument_spec=dict(
            count=dict(type='int', default=1),
            count_offset=dict(type='int', default=1),
            device_ids=dict(type='list', elements='str'),
            facility=dict(),
            features=dict(type='dict'),
            hostnames=dict(type='list', elements='str', aliases=['name']),
            tags=dict(type='list', elements='str'),
            locked=dict(type='bool', default=False, aliases=['lock']),
            operating_system=dict(),
            plan=dict(),
            state=dict(choices=ALLOWED_STATES, default='present'),
            user_data=dict(default=None),
            wait_for_public_IPv=dict(type='int', choices=[4, 6]),
            wait_timeout=dict(type='int', default=900),
            ipxe_script_url=dict(default=''),
            always_pxe=dict(type='bool', default=False),
        ),
        required_one_of=[('device_ids', 'hostnames',)],
        mutually_exclusive=[
            ('hostnames', 'device_ids'),
            ('count', 'device_ids'),
            ('count_offset', 'device_ids'),
        ]
    )

    if not HAS_METAL_SDK:
        module.fail_json(msg='packet-python required for this module')

    state = module.params.get('state')

    try:
        module.exit_json(**act_on_devices(module, state))
    except Exception as e:
        module.fail_json(msg='failed to set device state %s, error: %s' %
                         (state, to_native(e)), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
