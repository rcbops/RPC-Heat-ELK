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

from elasticsearch import Elasticsearch

log = logging.getLogger(__name__)

class TemplateTest(unittest.TestCase):
    config = {"openstack":   {
                              "user": "admin", 
                              "password": "secrete", 
                              "tenant_name": "admin",
                              "net_name": "public"
                             },
              "heat_params": {
                              "keyname": "heat-key",
                              "image": "Ubuntu 12.04 software config",
                              "minion-count-elk": 1,
                              "minion-flavor-elk": "m1.medium",
                              "kibana-user": "admin",
                              "kibana-passwd": "secrete"
                             }
             }

    @classmethod
    def setUpClass(self):
        self.stack_name = 'test_elk_stack'
        ostack_config = self.config['openstack']
        self.keystone = ksclient.Client(auth_url="http://127.0.0.1:35357/v2.0",
                                   username=ostack_config['user'],
                                   password=ostack_config['password'],
                                   tenant_name=ostack_config['tenant_name'])
        endpoints = self.keystone.service_catalog.get_endpoints(service_type='orchestration')
        endpoints.update(self.keystone.service_catalog.get_endpoints(service_type='network'))

        self.heat_endpoint = endpoints['orchestration'][0]['publicURL']
        self.neutron_endpoint = endpoints['network'][0]['publicURL']

        token = self.keystone.auth_token

        if self.heat_endpoint is None or self.neutron_endpoint is None:
            raise Exception('No endpoint found for either heat or neutron')

        neutron = neutron_client.Client('2.0', endpoint_url=self.neutron_endpoint, token=token)
        pub_net = neutron.list_networks(name=ostack_config['net_name'])['networks'][0]
        heat = heat_client('1', endpoint=self.heat_endpoint, token=token)

        heat_params = self.config['heat_params']
        heat_params['floating-network-id'] = pub_net['id']
        #params_list = {
        #    'keyname': 'heat-key',
        #    'image': 'Ubuntu 12.04 software config',
        #    'floating-network-id': pub_net['id'],
        #    'minion-count-elk': 1,
        #    'minion-flavor-elk': 'm1.medium',
        #    'kibana-user': 'admin',
        #    'kibana-passwd': 'secrete'
        #}
        
        fields = {
            'stack_name': self.stack_name,
            'timeout_mins': '120',
            'parameters': dict(heat_params)
        }

        template_data = ''
        with open('../elk-stack.yaml') as f:
            fields['template'] = f.read()

        with open('../env.yaml') as f:
            fields['environment'] = f.read()

        test_stack = heat.stacks.create(**fields)
        self.test_stack_id = test_stack['stack']['id']
        #self.test_stack_id = 'f9eec6db-cc62-4fe9-b5e7-5a49dc559fa1'

        while True:
            self.stack_info = heat.stacks.get(self.test_stack_id)
            if self.stack_info.stack_status == 'CREATE_IN_PROGRESS':
                time.sleep(10)
                log.debug("Waiting for stack completion")
            elif self.stack_info.stack_status == 'CREATE_COMPLETE':
                log.debug("Stack successful")
                break
            else:
                log.debug("Stack failed")
                raise Exception(self.stack_info.stack_status, 'Stack failed with reason: %s' % self.stack_info.stack_status_reason)


    @classmethod
    def tearDownClass(self):
        self.keystone.authenticate()
        token = self.keystone.auth_token
        heat = heat_client('1', endpoint=self.heat_endpoint, token=token)
        heat.stacks.delete(self.test_stack_id)

    @unittest.skip("test good. waiting to finish others")
    def test_elasticsearch(self):
        haproxy_ip = None
        for output in self.stack_info.outputs:
            if output['output_key'] == 'minion-haproxy-ip':
                haproxy_ip = output['output_value']

        if haproxy_ip is None:
            raise Exception("Unable to find IP of stack VM")

        es = Elasticsearch([haproxy_ip])
        doc = { "first_name" :  "Daniel", "last_name" : "Curran", "age" : 25, "about": "I like to compute", "interests":  [ "computers" ]}
        es.create( index='megacorp', doc_type='employee', id='1', body=doc )
        test_val = es.get(index='megacorp', doc_type='employee', id='1')
        return_doc = test_val['_source']
        self.assertTrue(test_val['found'])
        self.assertTrue(doc == return_doc)
         
        
    def test_logstash(self):
        
        print "LOGSTASH"
    
    #def test_kibana(self):
    #    pass

    def test_elk(self):
        print "TEST1"


if __name__ == '__main__':
    with open('test.yaml', 'r') as f:
        doc = yaml.load(f)
        TemplateTest.config = doc
    unittest.main()
    





