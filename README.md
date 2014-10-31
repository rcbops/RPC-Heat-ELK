Description
===========

This is an OpenStack HEAT template to deploy [ELK](http://www.elasticsearch.org/overview/) 
to a single server in an OpenStack cloud.

This template uses [elk salt-formulas](https://github.com/rcbops/elk-formula) 
to configure the servers. It deploys a salt-master, and a number of salt-minions. 
One minion will be the ELK node and one will be HAProxy for forwarding requests.

For access to kibana web UI, a floating ip will be assigned to the 
haproxy node. Or a new server can be created in the same network as the ELK network.

Requirements
============
* A Heat provider that supports the following:
  * OS::Neutron::Net
  * OS::Neutron::Subnet
  * OS::Neutron::Router
  * OS::Neutron::RouterInterface
  * OS::Neutron::FloatingIP
  * OS::Neutron::FloatingIPAssociation
  * OS::Neutron::Port
  * OS::Heat::SoftwareConfig
  * OS::Heat::SoftwareDeployment
  * OS::Heat::RandomString
  * OS::Heat::ResourceGroup
  * OS::Nova::Server
  * OS::Nova::KeyPair

* An Ubuntu image (12.04 or newer) preconfigured with heat-cfntools and heat confog-script. 
Instructions for creating a heat-cfntools enabled image for use with Heat can be 
found [here] (http://docs.openstack.org/developer/heat/getting_started/jeos_building.html).

* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.12`:

```bash
pip install python-heatclient
```
Heat-client Usage
=============
Here is an example of how to deploy this template using the
[python-heatclient](https://github.com/openstack/python-heatclient):

```
heat stack-create hadoop-stack -f hadoop-stack.yaml \
  -e env.yaml -P flavor=m1.large;floating-network-id=<NET_ID>; \
  datanodes-count=<COUNT>;keyname=<KEYNAME>;image=<IMAGE_ID>
```

Using Horizon
=============
You can also go to your Horizon Dashboard in your browser and create 
the Hadoop stack from under the Orchestration tab.

License
=======
```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
