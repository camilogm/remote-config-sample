class RemoteConfigProperty:
    def __init__(self, property_name: str, default_value: dict, value_type: str):
        self.property_name = property_name
        self.default_value = default_value
        self.value_type = value_type

    def __iter__(self):
        yield self.property_name
        yield self.default_value
        yield self.value_type