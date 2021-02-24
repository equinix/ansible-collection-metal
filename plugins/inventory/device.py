# (c) 2016, Peter Sankauskas
# (c) 2017, Tomas Karasek
# (c) 2021, Jason DeTiberus
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: device.py
    plugin_type: inventory
    short_description: Equinix Metal Device inventory source
    requirements:
        - "packet-python >= 1.43.1"
    extends_documentation_fragment:
        - equinix.metal.auth_options
        - inventory_cache
        - constructed
    description:
        - Get inventory hosts from the Equinix Metal Device API.
    author:
        - Peter Sankauskas
        - Tomas Karasek
        - Jason DeTiberus
    options:
        plugin:
            description: Token that ensures this is a source file for the plugin.
            required: True
            choices: ['equinix_metal', 'equinix.metal.device']
        projects:
          description:
              - A list of projects in which to describe Equinix Metal devices.
              - If empty (the default) default this will include all projects.
          type: list
          default: []
    version_added: 1.0.0
'''

EXAMPLES = '''
# Minimal example using environment var credentials
plugin: equinix.metal.device

# Example using constructed features to create groups and set ansible_host
plugin: equinix.metal.device
# keyed_groups may be used to create custom groups
strict: False
keyed_groups:
  # Add hosts to tag_Name groups for each tag
  - prefix: tag
    key: tags
  # Add hosts to e.g. equinix_metal_plan_c3_small_x86
  - prefix: equinix_metal_plan
    key: plan
  # Create a group per region e.g. equinix_metal_facility_am6
  - key: facility
    prefix: equinix_metal_facility
  # Create a group per device state e.g. equinix_metal_state_active
  - key: state
    prefix: equinix_metal_state
# Set individual variables with compose
compose:
  # Use the private IP address to connect to the host
  # (note: this does not modify inventory_hostname, which is set via I(hostnames))
  ansible_host: (ip_addresses | selectattr('address_family', 'equalto', 4) | selectattr('public', 'equalto', false) | first).address
'''

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils import six
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable, to_safe_group_name

try:
    import packet
    HAS_METAL = True
except ImportError:
    HAS_METAL = False


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'equinix_metal'

    def __init__(self):
        super(InventoryModule, self).__init__()

        self.group_prefix = 'equinix_metal'

        # credentials
        self.api_token = None

    def verify_file(self, path):
        '''
            :param loader: an ansible.parsing.dataloader.DataLoader object
            :param path: the path to the inventory config file
            :return the contents of the config file
        '''
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('equinix_metal.yml', 'equinix_metal.yaml')):
                return True
        self.display.debug("equinix_metal inventory filename must end with 'equinix_metal.yml' or 'equinix_metal.yaml'")
        return False

    def _set_credentials(self):
        '''
            :param config_data: contents of the inventory config file
        '''
        self.api_token = self.get_option('api_token')

    def _query(self, project_ids):
        '''
            :param project_ids: a list of project ids to query
        '''
        devices = []
        for id in project_ids:
            devices.extend(self._get_devices_by_project(id))

        return {'equinix_metal': devices}

    def _populate(self, groups):
        for group in groups:
            group = self.inventory.add_group(group)
            self._add_hosts(hosts=groups[group], group=group)
            self.inventory.add_child('all', group)

    def _add_hosts(self, hosts, group):
        '''
            :param hosts: a list of hosts to be added to a group
            :param group: the name of the group to which the hosts belong
        '''
        for host in hosts:
            hostname = host['hostname']

            self.inventory.add_host(hostname, group=group)
            for hostvar, hostval in host.items():
                self.inventory.set_variable(hostname, hostvar, hostval)

            # Use constructed if applicable
            strict = self.get_option('strict')

            # Composed variables
            self._set_composite_vars(self.get_option('compose'), host, hostname, strict=strict)

            # Complex groups based on jinja2 conditionals, hosts that meet the conditional are added to group
            self._add_host_to_composed_groups(self.get_option('groups'), host, hostname, strict=strict)

            # Create groups based on variable values and add the corresponding hosts to it
            self._add_host_to_keyed_groups(self.get_option('keyed_groups'), host, hostname, strict=strict)

    def parse(self, inventory, loader, path, cache=True):

        if not HAS_METAL:
            raise AnsibleParserError(
                'The Equinix Metal Device inventory plugin requires the python "packet-python" library'
            )

        super(InventoryModule, self).parse(inventory, loader, path)

        self._read_config_data(path)

        self._set_credentials()

        cache_key = self.get_cache_key(path)
        # false when refresh_cache or --flush-cache is used
        if cache:
            # get the user-specified directive
            cache = self.get_option('cache')

        # Generate inventory
        cache_needs_update = False
        if cache:
            try:
                results = self._cache[cache_key]
            except KeyError:
                # if cache expires or cache file doesn't exist
                cache_needs_update = True

        if not cache or cache_needs_update:
            project_ids = self._get_project_ids()
            results = self._query(project_ids)

        self._populate(results)

        # If the cache has expired/doesn't exist or if refresh_inventory/flush cache is used
        # when the user is using caching, update the cached inventory
        if cache_needs_update or (not cache and self.get_option('cache')):
            self._cache[cache_key] = results

    def _connect(self):
        ''' create connection to api server'''
        manager = packet.Manager(auth_token=self.api_token, consumer_token="ansible-equinix-metal-inventory")
        return manager

    def _get_project_ids(self):
        project_ids = self.get_option('projects')

        if not project_ids:
            try:
                manager = self._connect()
                projects = manager.list_projects()
                project_ids = [project.id for project in projects]
            except Exception as e:
                raise AnsibleError("Failed to query projects from Equinix Metal API", orig_exc=e)

        if not project_ids:
            raise AnsibleError('Unable to get projects list from available methods, you must specify the "projects" option to continue.')

        return project_ids

    def _get_devices_by_project(self, project_id):
        '''
           :param project_id: a project id in which to discover devices
           :return A list of device dictionaries
        '''
        try:
            manager = self._connect()
            devices = manager.list_devices(project_id=project_id)
            return [self._get_host_info_dict_from_device(device) for device in devices]
        except Exception as e:
            raise AnsibleError("Failed to query devices from Equinix Metal API", orig_exc=e)

    def _get_host_info_dict_from_device(self, device):
        device_vars = {}
        device.ip_addresses
        for key in vars(device):
            value = getattr(device, key)
            key = to_safe_group_name(key)

            # Handle complex types
            if key == 'state':
                device_vars[key] = device.state or ''
            elif key == 'hostname':
                device_vars[key] = value
            elif isinstance(value, (int, bool)):
                device_vars[key] = value
            elif isinstance(value, six.string_types):
                device_vars[key] = value.strip()
            elif value is None:
                device_vars[key] = ''
            elif key == 'facility':
                device_vars[key] = value['code']
            elif key == 'operating_system':
                device_vars[key] = value.slug
            elif key == 'plan':
                device_vars[key] = value['slug']
            elif key == 'project':
                device_vars[key] = value['href'].strip('/projects/')
            elif key == 'ip_addresses':
                device_vars[key] = []

                for addr in value:
                    device_vars[key].append(
                        {
                            'address': addr['address'],
                            'address_family': addr['address_family'],
                            'public': addr['public'],
                            'cidr': addr['cidr'],
                            'enabled': addr['enabled'],
                            'gateway': addr['gateway'],
                            'global_ip': addr['global_ip'],
                            'manageable': addr['manageable'],
                            'management': addr['management'],
                            'netmask': addr['netmask'],
                            'network': addr['network'],
                            'tags': addr['tags'],
                        }
                    )
            elif key == 'tags':
                device_vars[key] = value
            else:
                pass

        return device_vars
