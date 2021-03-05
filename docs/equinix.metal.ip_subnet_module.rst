.. _equinix.metal.ip_subnet_module:


***********************
equinix.metal.ip_subnet
***********************

**Assign IP subnet to a bare metal server.**


Version added: 1.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Assign or unassign IPv4 or IPv6 subnets to or from a device in Equinix Metal.
- IPv4 subnets must come from already reserved block.
- IPv6 subnets must come from publicly routable /56 block from your project.
- See https://metal.equinix.com/developers/docs/networking/elastic-ips/ for more info on IP block reservation.



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
                    <b>cidr</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 or IPv6 subnet which you want to manage. It must come from a reserved block for your project in the Packet Host.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: name</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>device_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>UUID of a device to/from which to assign/remove a subnet.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A hostname of a device to/from which to assign/remove a subnet.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>project_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>UUID of a project of the device to/from which to assign/remove a subnet.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>Desired state of the IP subnet on the specified device.</div>
                        <div>With state == <code>present</code>, you must specify either hostname or device_id. Subnet with given CIDR will then be assigned to the specified device.</div>
                        <div>With state == <code>absent</code>, you can specify either hostname or device_id. The subnet will be removed from specified devices.</div>
                        <div>If you leave both hostname and device_id empty, the subnet will be removed from any device it&#x27;s assigned to.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
    # You can also pass it to the api_token parameter of the module instead.

    - name: Create 1 device and assign an arbitrary public IPv4 subnet to it
      hosts: localhost
      tasks:

      - equinix.metal.device:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          hostnames: myserver
          operating_system: ubuntu_20_04
          plan: baremetal_0
          facility: sjc1
          state: active

    # Pick an IPv4 address from a block allocated to your project.

      - equinix.metal.ip_subnet:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          hostname: myserver
          cidr: "147.75.201.78/32"

    # Release IP address 147.75.201.78

    - name: Unassign IP address from any device in your project
      hosts: localhost
      tasks:
      - equinix.metal.ip_subnet:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          cidr: "147.75.201.78/32"
          state: absent



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
                    <b>changed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>True if an IP address assignments were altered in any way (created or removed).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>device_id</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>UUID of the device associated with the specified IP address.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>subnet</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Dict with data about the handled IP subnet.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;address&#x27;: &#x27;147.75.90.241&#x27;, &#x27;address_family&#x27;: 4, &#x27;assigned_to&#x27;: {&#x27;href&#x27;: &#x27;/devices/61f9aa5e-0530-47f5-97c2-113828e61ed0&#x27;}, &#x27;cidr&#x27;: 31, &#x27;created_at&#x27;: &#x27;2017-08-07T15:15:30Z&#x27;, &#x27;enabled&#x27;: True, &#x27;gateway&#x27;: &#x27;147.75.90.240&#x27;, &#x27;href&#x27;: &#x27;/ips/31eda960-0a16-4c0f-b196-f3dc4928529f&#x27;, &#x27;id&#x27;: &#x27;1eda960-0a16-4c0f-b196-f3dc4928529f&#x27;, &#x27;manageable&#x27;: True, &#x27;management&#x27;: True, &#x27;netmask&#x27;: &#x27;255.255.255.254&#x27;, &#x27;network&#x27;: &#x27;147.75.90.240&#x27;, &#x27;public&#x27;: True}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
- Nurfet Becirevic (@nurfet-becirevic) <nurfet.becirevic@gmail.com>
- Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
