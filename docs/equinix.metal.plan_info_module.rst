.. _equinix.metal.plan_info_module:


***********************
equinix.metal.plan_info
***********************

**Gather information about Equinix Metal plans**


Version added: 1.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Gather information about Equinix Metal plans.
- API is documented at https://metal.equinix.com/developers/api/plans/.



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
                    <b>ids</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>One or more plan ids.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>One or more plan names.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
    # You can also pass it to the api_token parameter of the module instead.

    - name: Gather information about all plans
      hosts: localhost
      tasks:
        - equinix.metal.plan_info:


    - name: Gather information about a particular plan using ID
      hosts: localhost
      tasks:
        - equinix.metal.plan_info:
          ids:
            - 173d7f11-f7b9-433e-ac40-f1571a38037a



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
                    <b>plans</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Information about each plan that was found</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{ &quot;id&quot;: &quot;e69c0169-4726-46ea-98f1-939c9e8a3607&quot;, &quot;name&quot;: &quot;t1.small.x86&quot;, &quot;description&quot;: &quot;Our Type 0 configuration is a general use &quot;cloud killer&quot; server, with a Intel Atom 2.4Ghz processor and 8GB of RAM.&quot;, &quot;available_in&quot;:[ &quot;ams1&quot;, &quot;ewr1&quot;, &quot;sjc1&quot;, &quot;nrt1&quot;, ], &quot;line&quot;: &quot;baremetal&quot;, &quot;pricing&quot;: { &quot;hour&quot;: 0.07 }, &quot;slug&quot;: &quot;baremetal_0&quot;, &quot;specs&quot;: { &quot;cpus&quot;: [ { &quot;count&quot;: 1, &quot;type&quot;: &quot;Intel Atom C2550 @ 2.4Ghz&quot; } ], &quot;drives&quot;: [ { &quot;count&quot;: 1, &quot;size&quot;: &quot;80GB&quot;, &quot;type&quot;: &quot;SSD&quot; } ], &quot;features&quot;: { &quot;raid&quot;: false, &quot;txt&quot;: true }, &quot;memory&quot;: { &quot;total&quot;: &quot;8GB&quot; }, &quot;nics&quot;: [ { &quot;count&quot;: 2, &quot;type&quot;: &quot;1Gbps&quot; } ] } }]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
