
# manual command line call to create firebase remote config client

from dotenv import load_dotenv
from firebase_remote_config_client import create_firebase_config_client
from dto.remote_config_property import RemoteConfigProperty


load_dotenv()

remote_config = create_firebase_config_client()


remote_config.get_parameters()
property = RemoteConfigProperty('from_python', {'value': 'new value value'}, 'STRING')
remote_config.modify_single_property(property)
remote_config.publish()