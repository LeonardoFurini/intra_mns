
import json
from utils.constants import Operations

class ConnParser():

    @staticmethod
    def create_request(operation: Operations, users: list = None, payload: str = None, origin: str = None) -> dict:
        return json.dumps({
            "operation": operation.value, 
            "users": users, 
            "payload": payload,
            "origin": origin
        })

    def decode_payload(str):
        pass
