import requests
import json
import boto3
import os
import io

from oauth2client.service_account import ServiceAccountCredentials

class FirebaseRemoteConfig:
    def __init__(self, base_url: str, remote_config_endpoint: str, remote_config_url) -> None:
        self.scopes = ['https://www.googleapis.com/auth/firebase.remoteconfig']
        self.base_url = base_url
        self.remote_config_endpoint = remote_config_endpoint
        self.remote_config_url = remote_config_url

    def _download_remote_service_account(self) -> str:
        service_account_json_path = os.environ.get('SERVICE_ACCOUNT_JSON_S3_PATH')
        bucket_name = os.environ.get('BUCKET_NAME')

        if (bucket_name is None):
            return 'service-account.json'

        if not service_account_json_path:
            raise ValueError("SERVICE_ACCOUNT_JSON_S3_PATH environment variable is not set.")
        
        service_account_path = '/tmp/service-account.json'
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, service_account_json_path, service_account_path)

        return service_account_path

    def _get_access_token(self):
        service_account_file = self._download_remote_service_account()
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            service_account_file, self.scopes)
        
        access_token_info = credentials.get_access_token()
        print('got access token')
        return access_token_info.access_token
    
    def _get_lastest_etag(self):
        headers = {
            'Authorization': 'Bearer ' + self._get_access_token()
        }
        resp = requests.get(self.remote_config_url, headers=headers)
        e_tag = resp.headers['ETag']
        return e_tag

    def _get_template(self):
        headers = {
            'Authorization': 'Bearer ' + self._get_access_token()
        }
        resp = requests.get(self.remote_config_url, headers=headers)

        if resp.status_code == 200:
            e_tag = resp.headers['ETag']
            print('ETag from server: {}'.format(resp.headers['ETag']))
            return (json.loads(resp.text), e_tag)
        else:
            print('Unable to get template')
            print(resp.text)  

    def _publish(self, etag, content):
        headers = {
            'Authorization': 'Bearer ' + self._get_access_token(),
            'Content-Type': 'application/json; UTF-8',
            'If-Match': etag
        }
        resp = requests.put(self.remote_config_url, data=content.encode('utf-8'), headers=headers)
        if resp.status_code == 200:
            print('Template has been published.')
            print('ETag from server: {}'.format(resp.headers['ETag']))
        else:
            print('Unable to publish template.')
            print(resp.text)
