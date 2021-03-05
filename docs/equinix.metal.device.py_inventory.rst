.. _equinix.metal.device.py_inventory:


***********************
equinix.metal.device.py
***********************

**Equinix Metal Device inventory source**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get inventory hosts from the Equinix Metal Device API.
- Uses a YAML configuration file that ends with equinix_metal.(yml|yaml).



Requirements
------------
The below requirements are needed on the local Ansible controller node that executes this inventory.

- packet-python >= 1.43.1


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>api_token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:METAL_API_TOKEN</div>
                                <div>env:PACKET_API_TOKEN</div>
                                <div>env:PACKET_TOKEN</div>
                    </td>
                <td>
                        <div>The Equinix Metal API token to use</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: auth_token</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cache</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[inventory]<br>cache = no</p>
                            </div>
                                <div>env:ANSIBLE_INVENTORY_CACHE</div>
                    </td>
                <td>
                        <div>Toggle to enable/disable the caching of the inventory&#x27;s source data, requires a cache plugin setup to work.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cache_connection</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>fact_caching_connection = VALUE</p>
                                    <p>[inventory]<br>cache_connection = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_CACHE_PLUGIN_CONNECTION</div>
                                <div>env:ANSIBLE_INVENTORY_CACHE_CONNECTION</div>
                    </td>
                <td>
                        <div>Cache connection data or path, read cache plugin documentation for specifics.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cache_plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"memory"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>fact_caching = memory</p>
                                    <p>[inventory]<br>cache_plugin = memory</p>
                            </div>
                                <div>env:ANSIBLE_CACHE_PLUGIN</div>
                                <div>env:ANSIBLE_INVENTORY_CACHE_PLUGIN</div>
                    </td>
                <td>
                        <div>Cache plugin to use for the inventory&#x27;s source data.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cache_prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"ansible_inventory_"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[default]<br>fact_caching_prefix = ansible_inventory_</p>
                                    <p>[inventory]<br>cache_prefix = ansible_inventory_</p>
                            </div>
                                <div>env:ANSIBLE_CACHE_PLUGIN_PREFIX</div>
                                <div>env:ANSIBLE_INVENTORY_CACHE_PLUGIN_PREFIX</div>
                    </td>
                <td>
                        <div>Prefix to use for cache plugin files/tables</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cache_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">3600</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>fact_caching_timeout = 3600</p>
                                    <p>[inventory]<br>cache_timeout = 3600</p>
                            </div>
                                <div>env:ANSIBLE_CACHE_PLUGIN_TIMEOUT</div>
                                <div>env:ANSIBLE_INVENTORY_CACHE_TIMEOUT</div>
                    </td>
                <td>
                        <div>Cache duration in seconds</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>compose</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Create vars from jinja2 expressions.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add hosts to group based on Jinja2 conditionals.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keyed_groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add hosts to group based on the values of a variable.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>equinix_metal</li>
                                    <li>equinix.metal.device</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Token that ensures this is a source file for the plugin.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>projects</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>A list of projects in which to describe Equinix Metal devices.</div>
                        <div>If empty (the default) default this will include all projects.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>strict</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>If <code>yes</code> make invalid entries a fatal error, otherwise skip and continue.</div>
                        <div>Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Peter Sankauskas
- Tomas Karasek
- Jason DeTiberus


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
