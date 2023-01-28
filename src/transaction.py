from dataclasses import dataclass
import json
import dataclasses as dc

# @dataclass
# class Transaction:
#     sender_address: int
#     receiver_address: int
#     value: float   

@dataclass
class Transaction:
    sender_address: str
    receiver_address: str
    value: float
    sign: str = None
        
    def str_data(self) -> str:
        # return the str of data without `sign`
        d=dc.asdict(self)
        del d["sign"]
        return json.dumps(d)
    
    def json_dumps(self) -> str:
        return json.dumps(dc.asdict(self))
    @classmethod
    def json_loads(cls, string) -> 'Transaction':
        return cls(**json.loads(string))