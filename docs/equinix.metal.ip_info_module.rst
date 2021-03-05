.. _equinix.metal.ip_info_module:


*********************
equinix.metal.ip_info
*********************

**Gather information about project IP Addresses**


Version added: 1.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Gather information about project IP addresses in Equinix Metal.
- See https://metal.equinix.com/developers/api/ipaddresses/ for more info on IP Addresses.



Requirements
------------
The below requirements are needed on the host that executes this module.

- packet-python >= 1.43.1


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
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
                        <div>The Equinix Metal API token to use</div>
                        <div>If not set, then the value of the METAL_API_TOKEN, PACKET_API_TOKEN, or PACKET_TOKEN environment variable is used.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: auth_token</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>project_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Project ID.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
    # You can also pass it to the api_token parameter of the module instead.

    - name: Gather information about all devices
      hosts: localhost
      tasks:
        - equinix.metal.ip_info:
            project_id: 89b497ee-5afc-420a-8fb5-56984898f4df



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>ips</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Information about each ip address that was found</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&quot;address&quot;: &quot;136.144.57.174&quot;, &quot;address_family&quot;: 4, &quot;assigned_to&quot;: null, &quot;cidr&quot;: 32, &quot;created_at&quot;: &quot;2021-01-05T18:55:55Z&quot;, &quot;customdata&quot;: {}, &quot;details&quot;: null, &quot;enabled&quot;: true, &quot;facility&quot;: &quot;dc13&quot;, &quot;gateway&quot;: &quot;136.144.57.174&quot;, &quot;global_ip&quot;: false, &quot;id&quot;: &quot;d6764db0-69c6-44e9-922e-18146608cd3a&quot;, &quot;interface&quot;: null, &quot;management&quot;: false, &quot;netmask&quot;: &quot;255.255.255.255&quot;, &quot;network&quot;: &quot;136.144.57.174&quot;, &quot;project_id&quot;: &quot;f2a2d7ad-886e-4207-bf38-10ebdf49cf84&quot;, &quot;public&quot;: true, &quot;tags&quot;: [&quot;cluster-api-provider-packet:cluster-id:versiontest&quot;]}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
