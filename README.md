# Ansible Collection - equinix.metal

[![CI](https://github.com/equinix/ansible-collection-metal/actions/workflows/ansible-integration.yml/badge.svg)](https://github.com/equinix/ansible-collection-metal/actions/workflows/ansible-integration.yml)[![Codecov](https://img.shields.io/codecov/c/github/equinix/ansible-collection-metal)](https://codecov.io/gh/equinix/ansible-collection-metal)

[![Depreacted](https://img.shields.io/badge/stability-deprecated-black.svg)](https://github.com/equinix/ansible-collection-metal/issues/59) [![Slack](https://slack.equinixmetal.com/badge.svg)](https://slack.equinixmetal.com/) [![Twitter Follow](https://img.shields.io/twitter/follow/equinixmetal.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=equinixmetal)

> [!IMPORTANT]
> This repository is [Deprecated](https://github.com/equinix-labs/equinix-labs/blob/master/deprecated-statement.md)!
>
> The Equinix Ansible Collection has been created to provide an interface to [Equinix APIs](https://developer.equinix.com/catalog) throughout the platform. Please transition to the Ansible Equinix Collection which has module parity with this Metal collection. The module names and parameters may differ slightly but the same backend APIs are utilized.  The Equinix Collection is backed by the more comprehensive and more maintainable [metal-python](https://github.com/equinix-labs/metal-python) SDK. This collection and metal-python follow upstream API naming and structures closely.
>
> * Equinix Deploy: <https://deploy.equinix.com/labs/ansible-collection-equinix/>
> * Ansible Collection: <https://galaxy.ansible.com/ui/repo/published/equinix/cloud/>
> * GitHub: [https://github.com/equinix-labs/ansible-collection-equinix](https://github.com/equinix-labs/ansible-collection-equinix#equinix-ansible-collection)

The Ansible Equinix Metal collection includes a variety of Ansible content to help automate the management of Equinix Metal resources. This collection is now deprecated.
<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Python version compatibility

This collection depends on [packet-python](https://github.com/packethost/packet-python). This collection requires Python 2.7 or greater.

## Included content

<!--start collection content-->
### Inventory plugins
Name | Description
--- | ---
[equinix.metal.device](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.device_inventory.rst)|Equinix Metal Device inventory source

### Modules
Name | Description
--- | ---
[equinix.metal.capacity_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.capacity_info_module.rst)|Gather information about Equinix Metal capacity
[equinix.metal.device](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.device_module.rst)|Manage a bare metal server in Equinix Metal
[equinix.metal.device_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.device_info_module.rst)|Gather information about Equinix Metal devices
[equinix.metal.facility_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.facility_info_module.rst)|Gather information about Equinix Metal facilities
[equinix.metal.ip_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.ip_info_module.rst)|Gather information about project IP Addresses
[equinix.metal.ip_subnet](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.ip_subnet_module.rst)|Assign IP subnet to a bare metal server.
[equinix.metal.operating_system_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.operating_system_info_module.rst)|Gather information about Equinix Metal operating_systems
[equinix.metal.org_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.org_info_module.rst)|Gather information about Equinix Metal organizations
[equinix.metal.plan_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.plan_info_module.rst)|Gather information about Equinix Metal plans
[equinix.metal.project](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.project_module.rst)|Create/delete a project in Equinix Metal
[equinix.metal.project_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.project_info_module.rst)|Gather information about Equinix Metal projects
[equinix.metal.sshkey](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.sshkey_module.rst)|Create/delete an SSH key in Equinix Metal
[equinix.metal.sshkey_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.sshkey_info_module.rst)|Gather information about Equinix Metal SSH keys
[equinix.metal.user_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.user_info_module.rst)|Gather information about the logged in user

<!--end collection content-->

## Installing this collection

You can install the Equinix Metal collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install equinix.metal

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: equinix.metal
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

    pip install -r requirements.txt

or:

    pip install packet-python

## Using this collection


You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `equinix.metal.device`, or you can call modules by their short name if you list the `equinix.metal` collection in the playbook's `collections` keyword:

```yaml
---
TODO
```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.


### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Equinix Metal collection repository](https://github.com/equinix/ansible-collection-metal).

If you require support, please email [support@equinixmetal.com](mailto:support@equinixmetal.com), visit the Equinix Metal IRC channel (#equinixmetal on freenode), subscribe to the [Equinix Metal Community Slack channel](https://slack.equinixmetal.com/) or post an issue within this repository.

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

### Testing with `ansible-test`

Running sanity tests: `ansible-test sanity --docker -v`
Running unit tests: `ansible-test units -v --docker`

Running integration tests:

```sh
cat << EOF > tests/integration/integration_config.yml
api_token: <YOUR EQUINIX METAL API TOKEN>
EOF
 ansible-test integration -v --docker
 ```

### More information about contributing

- [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) - Details on contributing to Ansible
- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly

## Release notes
<!--Add a link to a changelog.rst file or an external docsite to cover this information. -->

This project tags releases based on the Semantic Versioning specification. See <https://semver.org/#semantic-versioning-specification-semver> for more details. Please pin your dependencies accordingly.

Changes to this project can be reviewed in the [CHANGELOG.rst](https://github.com/equinix/ansible-collection-metal/blob/main/CHANGELOG.rst) file.

It is possible to follow changes to the changelog by subscribing to <https://github.com/equinix/ansible-collection-metal/releases.atom>, or "Watching" releases using the GitHub UI.

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## Publishing New Version

Prepare the release:
- Refresh the README.md: `tox -e add_docs`
- Refresh the changelog: `tox -e antsibull-changelog -- release --verbose --version 1.1.0`
- Clean up the changelog fragments.
- Commit everything and push a PR for review

Push the release:
- Tag the release: `git tag -s 1.0.0`
- Push the tag: `git push origin 1.0.0`

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
