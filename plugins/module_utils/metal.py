# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
import uuid

HAS_METAL_SDK = True
try:
    import packet
except ImportError:
    HAS_METAL_SDK = False

from ansible.module_utils.basic import AnsibleModule, env_fallback

NAME_RE = r'({0}|{0}{1}*{0})'.format(r'[a-zA-Z0-9]', r'[a-zA-Z0-9\-]')
HOSTNAME_RE = r'({0}\.)*{0}$'.format(NAME_RE)


class AnsibleMetalModule(object):
    """An ansible module class for Equinix Metal modules

    AnsibleMetalModule provides an a class for building modules which
    connect to Equinix Metal Services.  The interface is currently more
    restricted than the basic module class with the aim that later the
    basic module class can be reduced.  If you find that any key
    feature is missing please contact the author/Equinix Metal team
    (available on #equinixmetal on IRC) to request the additional
    features needed.
    """
    default_settings = {
        "default_args": True,
        "project_id_arg": True,
        "module_class": AnsibleModule
    }

    def __init__(self, **kwargs):
        local_settings = {}
        for key in AnsibleMetalModule.default_settings:
            try:
                local_settings[key] = kwargs.pop(key)
            except KeyError:
                local_settings[key] = AnsibleMetalModule.default_settings[key]
        self.settings = local_settings

        if local_settings["default_args"]:
            argument_spec_full = metal_argument_spec()
            try:
                argument_spec_full.update(kwargs["argument_spec"])
            except (TypeError, NameError):
                pass
            kwargs["argument_spec"] = argument_spec_full

        if local_settings["project_id_arg"]:
            argument_spec_full = metal_project_id_argument_spec()
            try:
                argument_spec_full.update(kwargs["argument_spec"])
            except (TypeError, NameError):
                pass
            kwargs["argument_spec"] = argument_spec_full

        self._module = AnsibleMetalModule.default_settings["module_class"](**kwargs)

        self.check_mode = self._module.check_mode
        self._diff = self._module._diff
        self._name = self._module._name

        if not HAS_METAL_SDK:
            self.fail_json(msg='python-packet required for this module')

        if local_settings["default_args"]:
            self.metal_conn = packet.Manager(auth_token=self.params.get('api_token'))

    def get_devices(self):
        project_id = self.params.get('project_id')
        if not is_valid_uuid(project_id):
            raise Exception("Project ID {0} does not seem to be valid".format(project_id))

        return self.metal_conn.list_all_devices(project_id)


    @property
    def params(self):
        return self._module.params

    def exit_json(self, *args, **kwargs):
        return self._module.exit_json(*args, **kwargs)

    def fail_json(self, *args, **kwargs):
        return self._module.fail_json(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self._module.debug(*args, **kwargs)

    def warn(self, *args, **kwargs):
        return self._module.warn(*args, **kwargs)

    def deprecate(self, *args, **kwargs):
        return self._module.deprecate(*args, **kwargs)

    def boolean(self, *args, **kwargs):
        return self._module.boolean(*args, **kwargs)

    def md5(self, *args, **kwargs):
        return self._module.md5(*args, **kwargs)


def metal_argument_spec():
    return dict(
        api_token=dict(
            type='str',
            fallback=(env_fallback, ['METAL_API_TOKEN', 'PACKET_API_TOKEN', 'PACKET_TOKEN']),
            no_log=True,
            aliases=['auth_token'],
            required=True
        ),
    )


def metal_project_id_argument_spec():
    return dict(
        project_id=dict(required=True),
    )


def is_valid_hostname(hostname):
    return re.match(HOSTNAME_RE, hostname) is not None


def is_valid_uuid(myuuid):
    try:
        val = uuid.UUID(myuuid, version=4)
    except ValueError:
        return False
    return str(val) == myuuid


def serialize_device(device):
    """
    Standard representation for a device as returned by various tasks::

        {
            'id': 'device_id'
            'hostname': 'device_hostname',
            'tags': [],
            'locked': false,
            'state': 'provisioning',
            'ip_addresses': [
                {
                    "address": "147.75.194.227",
                    "address_family": 4,
                    "public": true
                },
                {
                    "address": "2604:1380:2:5200::3",
                    "address_family": 6,
                    "public": true
                },
                {
                    "address": "10.100.11.129",
                    "address_family": 4,
                    "public": false
                }
            ],
            "private_ipv4": "10.100.11.129",
            "public_ipv4": "147.75.194.227",
            "public_ipv6": "2604:1380:2:5200::3",
        }

    """
    device_data = {}
    device_data['id'] = device.id
    device_data['hostname'] = device.hostname
    device_data['tags'] = device.tags
    device_data['locked'] = device.locked
    device_data['state'] = device.state
    device_data['ip_addresses'] = [
        {
            'address': addr_data['address'],
            'address_family': addr_data['address_family'],
            'public': addr_data['public'],
        }
        for addr_data in device.ip_addresses
    ]
    # Also include each IPs as a key for easier lookup in roles.
    # Key names:
    # - public_ipv4
    # - public_ipv6
    # - private_ipv4
    # - private_ipv6 (if there is one)
    for ipdata in device_data['ip_addresses']:
        if ipdata['public']:
            if ipdata['address_family'] == 6:
                device_data['public_ipv6'] = ipdata['address']
            elif ipdata['address_family'] == 4:
                device_data['public_ipv4'] = ipdata['address']
        elif not ipdata['public']:
            if ipdata['address_family'] == 6:
                # Packet doesn't give public ipv6 yet, but maybe one
                # day they will
                device_data['private_ipv6'] = ipdata['address']
            elif ipdata['address_family'] == 4:
                device_data['private_ipv4'] = ipdata['address']
    return device_data


def serialize_project(project):
    """
    Standard representation for a project as returned by various tasks::

        {
            'id': 'project_id',
            'name': 'project_name'
        }

    """
    return dict(
        id=project.id,
        name=project.name,
    )


def serialize_sshkey(sshkey):
    """
    Standard representation for an ssh key as returned by various tasks::

        {
            "fingerprint": "5c:93:74:7c:ed:07:17:62:28:75:79:23:d6:08:93:46",
            "id": "41d61bd8-3342-428b-a09c-e67bdd18a9b7",
            "key": "ssh-dss AAAAB3NzaC1kc3MAAACBAIfNT5S0ncP4BBJBYNhNPxFF9lqVhfPeu6SM1LoCocxqDc1AT3zFRi8hjIf6TLZ2AA4FYbcAWxLMhiBxZRVldT9GdBXile78kAK5z3bKTwq152DCqpxwwbaTIggLFhsU8wrfBsPWnDuAxZ0h7mmrCjoLIE3CNLDA/NmV3iB8xMThAAAAFQCStcesSgR1adPORzBxTr7hug92LwAAAIBOProm3Gk+HWedLyE8IfofLaOeRnbBRHAOL4z0SexKkVOnQ/LGN/uDIIPGGBDYTvXgKZT+jbHeulRJ2jKgfSpGKN4JxFQ8uzVH492jEiiUJtT72Ss1dCV4PmyERVIw+f54itihV3z/t25dWgowhb0int8iC/OY3cGodlmYb3wdcQAAAIBuLbB45djZXzUkOTzzcRDIRfhaxo5WipbtEM2B1fuBt2gyrvksPpH/LK6xTjdIIb0CxPu4OCxwJG0aOz5kJoRnOWIXQGhH7VowrJhsqhIc8gN9ErbO5ea8b1L76MNcAotmBDeTUiPw01IJ8MdDxfmcsCslJKgoRKSmQpCwXQtN2g== tomk@hp2",
            "label": "mynewkey33"
        }
    """  # noqa
    sshkey_data = {}
    copy_keys = ['id', 'key', 'label', 'fingerprint']
    for name in copy_keys:
        sshkey_data[name] = getattr(sshkey, name)
    return sshkey_data


