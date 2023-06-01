import json
from server.models import *




# ----------- Package Serialization -----------
class PackageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Package):
            return {"from": obj.dest, "to": obj.to, 
                    "type": obj.type, "data": obj.data}
        return super().default(obj)
    
class PackageDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if 'dest' in dct and 'to' in dct and \
            'type' in dct and 'data' in dct:
            return Package(dest=dct["dest"], to=dct["to"],
                        type=dct["type"], data=dct["data"])
        return dct