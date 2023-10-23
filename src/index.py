import json
from dotenv import load_dotenv
from firebase_remote_config_client import create_firebase_config_client
from dto.remote_config_property import RemoteConfigProperty


# Load environment variables from .env into the environment
load_dotenv()

remote_config = create_firebase_config_client()

def lambda_handler(event, context):
    # Parse the data from the Lambda event
    if (isinstance(event['body'], str)):
            data = json.loads(event["body"])
    else:
         data = event['body']


    if (not 'name' in data or not 'value' in data):
        return {
            "statusCode": 400,
            "body": json.dumps("Missing required parameters (name, value)"),
        }

    # Modify Remote Config properties
    property = RemoteConfigProperty(data['name'], {'value': data['value']}, 'STRING')
    remote_config.modify_single_property(property)
    remote_config.publish()

    return {
        "statusCode": 200,
        "body": json.dumps("Remote Config properties modified and published successfully"),
    }

