import unittest
import json
import keystoneclient
import yaml
from uuid import uuid4
from nose import SkipTest
from string import letters

#from keystoneclient.auth.identity import v3
#from keystoneclient import session
#from keystoneclient.v3 import client
#from keystoneclient import client
import keystoneclient.v2_0.client as ksclient
import heatclient
from heatclient.client import Client


class TestTemplate(unittest.TestCase):
    param_prefix = '__param_'

    def setUp(self):
        keystone = ksclient.Client(auth_url="http://127.0.0.1:35357/v2.0",
                           username="admin",
                           password="secrete",
                           tenant_name="admin")
        token = keystone.auth_ref['token']['id']
        tenant_id = keystone.tenant_id
        heat_endpoint = None
        
        for service in keystone.auth_ref['serviceCatalog']:
            if service['name'] == 'heat':
                heat_endpoint = service['endpoints'][0]['publicURL']
                break
        
        if heat_endpoint is None:
            raise Exception('No heat endpoint found')

        heat = Client('1', endpoint=heat_endpoint, token=token)
        params_list = [
            ('keyname', 'heat_test_key'),
            ('image', 'HeatImage'),
            ('floating-network-id', 'f8b75425-ab2e-41db-b18f-b38a36fbc8e7'),
            ('minion-count-elk', 1),
            ('minion-flavor-elk', 'm1.medium'),
            ('kibana-user', 'admin'),
            ('kibana-passwd', 'secrete')
        ]


        
        fields = {
            'stack_name': 'test_elk_stack',
            'timeout_mins': '120',
            'parameters': dict(params_list),
        }

        template_data = ''
        with open('../elk-stack.yaml') as f:
            fields['template'] = f.readlines()

        with open('../env.yaml') as f:
            fields['environment'] = f.readlines()
        
        heat.stacks.create(**fields)
        

    def tearDown(self):
        pass        

    def test_metadata(self):
        pass


if __name__ == '__main__':
    with open('test.yaml', 'r') as f:
        doc = yaml.load(f)
    unittest.main()
