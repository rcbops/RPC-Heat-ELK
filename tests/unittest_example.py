import unittest
import json
import ConfigParser
import keystoneclient

from uuid import uuid4
from nose import SkipTest
from string import letters

from keystoneclient.v3 import client

class TestTemplate(unittest.TestCase):

    def setUp(self):
        auth = v3.Password(auth_url='https://my.keystone.com:5000/v3',
            user_id='myuserid',
            password='mypassword',
             project_id='myprojectid')
        sess = session.Session(auth=auth)
        keystone = client.Client(session=sess)
        

    def tearDown(self):
        

    def test_metadata(self):



if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read("/opt/openrc")
    openstack_config = config("openstack_config")

    unittest.main()
