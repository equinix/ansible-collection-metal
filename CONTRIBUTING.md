# Contributing

## Getting Started

General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).

## Equinix Collections

There is currently a single collection containing Equinix Metal content (modules and plugins).

### equinix.metal

The `equinix.metal` collection is an Equinix Metal-maintained collection.

## Submitting Issues
All software has bugs, and the `equinix.metal` collection is no exception. When you find a bug, 
you can help tremendously by [telling us about it](https://github.com/equinix/ansible-collection-metal/issues/new/choose).

If you should discover that the bug you're trying to file already exists in an issue, 
you can help by verifying the behavior of the reported bug with a comment in that 
issue, or by reporting any additional information

## Pull Requests

All modules MUST have integration tests for new features.
Bug fixes for modules that currently have integration tests SHOULD have tests added.  
New modules MUST have integration tests.

Expected test criteria:
* Resource creation under check mode
* Resource creation
* Resource creation again (idempotency) under check mode
* Resource creation again (idempotency)
* Resource modification under check mode
* Resource modification
* Resource modification again (idempotency) under check mode
* Resource modification again (idempotency)
* Resource deletion under check mode
* Resource deletion
* Resource deletion (of a non-existent resource) under check mode
* Resource deletion (of a non-existent resource)

Where modules have multiple parameters we recommend running through the 4-step modification cycle for each parameter the module accepts, as well as a modification cycle where as most, if not all, parameters are modified at the same time.

For general information on running the integration tests see the
[Integration Tests page of the Module Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/testing_integration.html#testing-integration),
especially the section on configuration for cloud tests.  For questions about writing tests the Equinix Metal community can
be found as detailed below.


### Code of Conduct
The `equinix.metal` collection follows the Ansible project's 
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html). 
Please read and familiarize yourself with this document.

### Contact Information
If you require support, please email [support@equinixmetal.com](mailto:support@equinixmetal.com), visit the Equinix Metal IRC channel (#equinixmetal on freenode), subscribe to the [Equinix Metal Community Slack channel](https://slack.equinixmetal.com/) or post an issue within this repository.
