from dataclasses import dataclass

@dataclass
class Transaction:
    sender_address: int
    receiver_address: int
    value: float 
