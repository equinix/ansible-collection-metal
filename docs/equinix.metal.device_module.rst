.. _equinix.metal.device_module:


********************
equinix.metal.device
********************

**Manage a bare metal server in Equinix Metal**


Version added: 1.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage a bare metal server in Equinix Metal (a "device" in the API terms).
- When the machine is created it can optionally wait for public IP address, or for active state.
- API is documented at https://metal.equinix.com/developers/api/devices/.



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
                    <b>always_pxe</b>
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
                        <div>Persist PXE as the first boot option.</div>
                        <div>Normally, the PXE process happens only on the first boot. Set this arg to have your device continuously boot to iPXE.</div>
                </td>
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
                    <b>count</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">1</div>
                </td>
                <td>
                        <div>The number of devices to create. Count number can be included in hostname via the %d string formatter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>count_offset</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">1</div>
                </td>
                <td>
                        <div>From which number to start the count.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>device_ids</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of device IDs on which to operate.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>facility</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Facility slug for device creation. See the Equinix Metal API for current list - <a href='https://metal.equinix.com/developers/api/facilities/'>https://metal.equinix.com/developers/api/facilities/</a>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>features</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Dict with &quot;features&quot; for device creation. See Equinix Metal API docs for details.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hostnames</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A hostname of a device, or a list of hostnames.</div>
                        <div>If given string or one-item list, you can use the <code>&quot;%d&quot;</code> Python string format to expand numbers from <em>count</em>.</div>
                        <div>If only one hostname, it might be expanded to list if <em>count</em>&gt;1.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: name</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipxe_script_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>URL of custom iPXE script for provisioning.</div>
                        <div>More about custom iPXE for Equinix Metal devices at <a href='https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/'>https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/</a>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>locked</b>
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
                        <div>Whether to lock a created device.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: lock</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>operating_system</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>OS slug for device creation. See Equinix Metal API for current list - <a href='https://metal.equinix.com/developers/api/operatingsystems/'>https://metal.equinix.com/developers/api/operatingsystems/</a>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Plan slug for device creation. See Equinix Metal API for current list - <a href='https://metal.equinix.com/developers/api/plans/'>https://metal.equinix.com/developers/api/plans/</a>.</div>
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
                                    <li>active</li>
                                    <li>inactive</li>
                                    <li>rebooted</li>
                        </ul>
                </td>
                <td>
                        <div>Desired state of the device.</div>
                        <div>If set to <code>present</code> (the default), the module call will return immediately after the device-creating HTTP request successfully returns.</div>
                        <div>If set to <code>active</code>, the module call will block until all the specified devices are in state active, or until <em>wait_timeout</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tags</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of device tags.</div>
                        <div>Currently implemented only for device creation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user_data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Userdata blob made available to the machine</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wait_for_public_IPv</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>4</li>
                                    <li>6</li>
                        </ul>
                </td>
                <td>
                        <div>Whether to wait for the instance to be assigned a public IPv4/IPv6 address.</div>
                        <div>If set to 4, it will wait until IPv4 is assigned to the instance.</div>
                        <div>If set to 6, wait until public IPv6 is assigned to the instance.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wait_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">900</div>
                </td>
                <td>
                        <div>How long (seconds) to wait either for automatic IP address assignment, or for the device to reach the <code>active</code> <em>state</em>.</div>
                        <div>If <em>wait_for_public_IPv</em> is set and <em>state</em> is <code>active</code>, the module will wait for both events consequently, applying the timeout twice.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Doesn't support check mode.



Examples
--------

.. code-block:: yaml

    # All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
    # You can also pass it to the api_token parameter of the module instead.

    # Creating devices

    - name: Create 1 device
      hosts: localhost
      tasks:
      - equinix.metal.device:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          hostnames: myserver
          tags: ci-xyz
          operating_system: ubuntu_16_04
          plan: baremetal_0
          facility: sjc1

    # Create the same device and wait until it is in state "active", (when it's
    # ready for other API operations). Fail if the device is not "active" in
    # 10 minutes.

    - name: Create device and wait up to 10 minutes for active state
      hosts: localhost
      tasks:
      - equinix.metal.device:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          hostnames: myserver
          operating_system: ubuntu_16_04
          plan: baremetal_0
          facility: sjc1
          state: active
          wait_timeout: 600

    - name: Create 3 ubuntu devices called server-01, server-02 and server-03
      hosts: localhost
      tasks:
      - equinix.metal.device:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          hostnames: server-%02d
          count: 3
          operating_system: ubuntu_16_04
          plan: baremetal_0
          facility: sjc1

    - name: Create 3 coreos devices with userdata, wait until they get IPs and then wait for SSH
      hosts: localhost
      tasks:
      - name: Create 3 devices and register their facts
        equinix.metal.device:
          hostnames: [coreos-one, coreos-two, coreos-three]
          operating_system: coreos_stable
          plan: baremetal_0
          facility: ewr1
          locked: true
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          wait_for_public_IPv: 4
          user_data: |
            #cloud-config
            ssh_authorized_keys:
              - {{ lookup('ansible.builtin.file', 'my_equinix_metal_sshkey') }}
            coreos:
              etcd:
                discovery: https://discovery.etcd.io/6a28e078895c5ec737174db2419bb2f3
                addr: $private_ipv4:4001
                peer-addr: $private_ipv4:7001
              fleet:
                public-ip: $private_ipv4
              units:
                - name: etcd.service
                  command: start
                - name: fleet.service
                  command: start
        register: newhosts

      - name: Wait for ssh
        ansible.builtin.wait_for:
          delay: 1
          host: "{{ item.public_ipv4 }}"
          port: 22
          state: started
          timeout: 500
        with_items: "{{ newhosts.devices }}"


    # Other states of devices

    - name: Remove 3 devices by uuid
      hosts: localhost
      tasks:
      - equinix.metal.device:
          project_id: 89b497ee-5afc-420a-8fb5-56984898f4df
          state: absent
          device_ids:
            - 1fb4faf8-a638-4ac7-8f47-86fe514c30d8
            - 2eb4faf8-a638-4ac7-8f47-86fe514c3043
            - 6bb4faf8-a638-4ac7-8f47-86fe514c301f



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
                            <div>True if a device was altered in any way (created, modified or removed)</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>devices</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Information about each device that was processed</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&quot;hostname&quot;: &quot;my-server.com&quot;, &quot;id&quot;: &quot;2a5122b9-c323-4d5c-b53c-9ad3f54273e7&quot;, &quot;public_ipv4&quot;: &quot;147.229.15.12&quot;, &quot;private-ipv4&quot;: &quot;10.0.15.12&quot;, &quot;tags&quot;: [], &quot;locked&quot;: false, &quot;state&quot;: &quot;provisioning&quot;, &quot;public_ipv6&quot;: &quot;&quot;2604:1380:2:5200::3&quot;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
- Matt Baldwin (@baldwinSPC) <baldwin@stackpointcloud.com>
- Thibaud Morel l'Horset (@teebes) <teebes@gmail.com>
- Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
