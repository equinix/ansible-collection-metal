# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from ansible.module_utils.basic import AnsibleModule


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

    def get_api_token(self):
        api_token = self.params.get('api_token')

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
        api_token=dict(no_log=True, aliases=['auth_token']),
    )


def metal_project_id_argument_spec():
    return dict(
        project_id=dict(required=True),
    )
