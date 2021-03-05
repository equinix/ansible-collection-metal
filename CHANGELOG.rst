===========================
Equinix.Metal Release Notes
===========================

.. contents:: Topics


v1.4.0
======

Minor Changes
-------------

- device - The device inventory plugin now lists all devices rather than just up to the default page size
- device - The device module now lists all devices rather than just up to 100
- device_info - The device info module now lists all devices rather than just up to 100

New Modules
-----------

- equinix.metal.capacity_info - Gather information about Equinix Metal capacity
- equinix.metal.facility_info - Gather information about Equinix Metal facilities
- equinix.metal.ip_info - Gather information about project IP Addresses
- equinix.metal.ip_subnet - Assign IP subnet to a bare metal server.
- equinix.metal.operating_system_info - Gather information about Equinix Metal operating_systems
- equinix.metal.org_info - Gather information about Equinix Metal organizations
- equinix.metal.plan_info - Gather information about Equinix Metal plans
- equinix.metal.user_info - Gather information about the logged in user

v1.3.0
======

Bugfixes
--------

- device - Fix name for device inventory plugin

New Modules
-----------

- equinix.metal.sshkey - Create/delete an SSH key in Equinix Metal
- equinix.metal.sshkey_info - Gather information about Equinix Metal SSH keys

v1.2.0
======

New Modules
-----------

- equinix.metal.device_info - Gather information about Equinix Metal devices
- equinix.metal.project - Create/delete a project in Equinix Metal
- equinix.metal.project_info - Gather information about Equinix Metal projects

v1.1.0
======

New Modules
-----------

- equinix.metal.device - Manage a bare metal server in Equinix Metal

v1.0.0
======

New Plugins
-----------

Inventory
~~~~~~~~~

- equinix.metal.device - Equinix Metal Device inventory source
