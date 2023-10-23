import firebase_remote_config
import os
from dto.remote_config_property import RemoteConfigProperty
import json

class FirebaseRemoteConfigClient:
    def __init__(self, firebase_remote_config: firebase_remote_config.FirebaseRemoteConfig) -> None:
        self.firebase_remote_config = firebase_remote_config
        (template, e_tag) = self.firebase_remote_config._get_template()
        self.template = template
        self.e_tag = e_tag

    def get_parameters(self):
        return self.template['parameters']

    def modify_single_property(self, property: RemoteConfigProperty) -> None:
        self.template['parameters'][property.property_name] = {
            'defaultValue': property.default_value,
            'valueType': property.value_type,
        }

    def publish(self):
        self.e_tag = self.firebase_remote_config._get_lastest_etag()
        print(self.e_tag)
        self.firebase_remote_config._publish(self.e_tag, json.dumps(self.template))

def create_firebase_config_client():
    PROJECT_ID = os.environ.get('PROJECT_ID')
    base_url = 'https://firebaseremoteconfig.googleapis.com'
    remote_config_endpoint = 'v1/projects/' + PROJECT_ID + '/remoteConfig'
    remote_config_url = base_url + '/' + remote_config_endpoint

    firebase_remote_config_instance = firebase_remote_config.FirebaseRemoteConfig(base_url, remote_config_endpoint, remote_config_url)
    firebase_remote_config_client = FirebaseRemoteConfigClient(firebase_remote_config_instance)
    print('created firebase remote config client')
    return firebase_remote_config_client