# Copyright: (c) 2021, Equinix Metal
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
    options:
        api_token:
            description: The Equinix Metal API token to use
            required: True
            type: str
            env:
                - name: METAL_API_TOKEN
                - name: PACKET_API_TOKEN
                - name: PACKET_TOKEN
    '''
