# Copyright: (c) 2021, Equinix Metal
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
    options:
        api_token:
            description:
                - The Equinix Metal API token to use
                - If not set, then the value of the METAL_API_TOKEN, PACKET_API_TOKEN, or PACKET_TOKEN environment variable is used.
            type: str
            required: true
            aliases:
                - auth_token
    requirements:
        - "packet-python >= 1.43.1"
    '''
