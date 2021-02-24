# Ansible Collection - equinix.metal

![](https://img.shields.io/badge/stability-maintained-green.svg) [![Slack](https://slack.equinixmetal.com/badge.svg)](https://slack.equinixmetal.com/) [![Twitter Follow](https://img.shields.io/twitter/follow/equinixmetal.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=equinixmetal)

This repository is [Maintained](https://github.com/packethost/standards/blob/master/maintained-statement.md)!

The Ansible Equinix Metal collection includes a variety of Ansible content to help automate the management of Equinix Metal resources. This collection is maintained by the Equinix Metal team.

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
[equinix.metal.device.py](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.device.py_inventory.rst)|Equinix Metal Device inventory source

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
project_id: <EQUINIX METAL PROJECT ID TO RUN TESTS AGAINST>
EOF
 ansible-test integration -v --docker
 ```

### More information about contributing

- [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) - Details on contributing to Ansible
- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly

## Release notes
<!--Add a link to a changelog.rst file or an external docsite to cover this information. -->

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
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
