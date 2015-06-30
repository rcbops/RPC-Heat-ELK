import json
import keystoneclient
import logging
import time
import unittest
import yaml

from uuid import uuid4
from nose import SkipTest
from string import letters

import keystoneclient.v2_0.client as ksclient
import heatclient
from heatclient.client import Client as heat_client
from neutronclient.neutron import client as neutron_client

log = logging.getLogger(__name__)

class TestTemplate(unittest.TestCase):
    param_prefix = '__param_'
    stack_name = 'test_elk_stack'
    keystone = ksclient.Client(auth_url="http://127.0.0.1:35357/v2.0",
		   username="admin",
		   password="secrete",
		   tenant_name="admin")
    endpoints = keystone.service_catalog.get_endpoints(service_type='orchestration')
    endpoints.update(keystone.service_catalog.get_endpoints(service_type='network'))

    heat_endpoint = endpoints['orchestration'][0]['publicURL']
    neutron_endpoint = endpoints['network'][0]['publicURL']

    @classmethod
    def setUpClass(self):
        token = self.keystone.auth_token

        if self.heat_endpoint is None or self.neutron_endpoint is None:
            raise Exception('No endpoint found for either heat or neutron')

        neutron = neutron_client.Client('2.0', endpoint_url=self.neutron_endpoint, token=token)
        pub_net = neutron.list_networks(name="public")['networks'][0]
        heat = heat_client('1', endpoint=self.heat_endpoint, token=token)
        params_list = {
            'keyname': 'heat-key',
            'image': 'Ubuntu 12.04 software config',
            'floating-network-id': pub_net['id'],
            'minion-count-elk': 1,
            'minion-flavor-elk': 'm1.medium',
            'kibana-user': 'admin',
            'kibana-passwd': 'secrete'
        }
        
        fields = {
            'stack_name': self.stack_name,
            'timeout_mins': '120',
            'parameters': dict(params_list),
        }

        template_data = ''
        with open('../elk-stack.yaml') as f:
            fields['template'] = f.read()

        with open('../env.yaml') as f:
            fields['environment'] = f.read()

        test_stack = heat.stacks.create(**fields)
        self.test_stack_id = test_stack['stack']['id']

        while True:
            stack_info = heat.stacks.get(self.test_stack_id)
            if stack_info.stack_status == 'CREATE_IN_PROGRESS':
                time.sleep(10)
                log.debug("Waiting for stack completion")
            elif stack_info.stack_status == 'CREATE_COMPLETE':
                log.debug("Stack successful")
                break
            else:
                log.debug("Stack failed")
                raise Exception(stack_info.stack_status, 'Stack failed with reason: %s' % stack_info.stack_status_reason)

        print heat.stacks.get(self.test_stack_id)
        
    @classmethod
    def tearDownClass(self):
        self.keystone.authenticate()
        token = self.keystone.auth_token
        heat = heat_client('1', endpoint=self.heat_endpoint, token=token)
        heat.stacks.delete(self.test_stack_id)

    #def test_elasticsearch(self):
    #    pass

    #def test_kibana(self):
    #    pass

    #def test_logstash(self):
    #    pass

    def test_elk(self):
        print "TEST1"


if __name__ == '__main__':
    with open('test.yaml', 'r') as f:
        doc = yaml.load(f)
    unittest.main()

