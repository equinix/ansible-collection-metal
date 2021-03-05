.. _equinix.metal.user_info_module:


***********************
equinix.metal.user_info
***********************

**Gather information about the logged in user**


Version added: 1.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Gather information about the logged in user for Equinix Metal.
- See https://metal.equinix.com/developers/api/users/#retrieve-the-current-user for more info on users.



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
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
    # You can also pass it to the api_token parameter of the module instead.

    - name: Gather information about the current logged in user
      hosts: localhost
      tasks:
        - equinix.metal.user_info:



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
                    <b>user</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Information about the logged in user.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{ &quot;avatar_thumb_url&quot;: &quot;https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm&quot;, &quot;avatar_url&quot;: &quot;https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm&quot;, &quot;created_at&quot;: &quot;2021-02-26T14:08:17Z&quot;, &quot;customdata&quot;: {}, &quot;default_organization_id&quot;: &quot;594b06f3-cef2-4127-85fd-08332fcf0021&quot;, &quot;default_project_id&quot;: null, &quot;email&quot;: &quot;does@not.exist&quot;, &quot;emails&quot;: [ { &quot;href&quot;: &quot;/emails/7c281a6b-1801-4008-89f3-0a43a2fb26e1&quot; } ], &quot;features&quot;: [ &quot;maintenance_mail&quot;, &quot;deploy_without_public_ip&quot;, &quot;advanced_ips&quot;, &quot;block_storage&quot;, &quot;bgp_default_route&quot;, &quot;native_vlan&quot;, ], &quot;first_name&quot;: &quot;Does&quot;, &quot;full_name&quot;: &quot;Does Not Exist&quot;, &quot;href&quot;: &quot;/users/7867d973-9b75-48dc-b94f-0d0a87e9dda0&quot;, &quot;id&quot;: &quot;7867d973-9b75-48dc-b94f-0d0a87e9dda0&quot;, &quot;language&quot;: null, &quot;last_login_at&quot;: &quot;2021-03-02T21:48:07Z&quot;, &quot;last_name&quot;: &quot;Not Exist&quot;, &quot;mailing_address&quot;: null, &quot;max_projects&quot;: 0, &quot;number_of_ssh_keys&quot;: 0, &quot;opt_in&quot;: false, &quot;opt_in_updated_at&quot;: null, &quot;phone_number&quot;: null, &quot;restricted&quot;: false, &quot;short_id&quot;: &quot;7867d973&quot;, &quot;social_accounts&quot;: {}, &quot;timezone&quot;: &quot;America/New_York&quot;, &quot;two_factor_auth&quot;: &quot;&quot;, &quot;updated_at&quot;: &quot;2021-03-02T08:23:18Z&quot;, &quot;verification_stage&quot;: &quot;verified&quot;, &quot;vpn&quot;: false }</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
