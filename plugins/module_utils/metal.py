# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os


def get_api_token(module):
    api_token = module.params.get('api_token')

    if not api_token:
        if os.environ.get('METAL_API_TOKEN'):
            api_token = os.environ['METAL_API_TOKEN']
        elif os.environ.get('PACKET_API_TOKEN'):
            api_token = os.environ['PACKET_API_TOKEN']
        elif os.environ.get('PACKET_TOKEN'):
            api_token = os.environ['PACKET_TOKEN']
        else:
            # in case api_token came in as empty string
            api_token = None

    return api_token
