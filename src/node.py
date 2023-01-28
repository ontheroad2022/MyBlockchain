from time import sleep
from blockchain import BlockChain
from block import Block
from uuid import uuid4
from time import time
from copy import deepcopy
from itertools import count

class Node:
    def __init__(self, network, genesis, uuid=None):
        self.chain=BlockChain([genesis])
        self.uuid=uuid or str(uuid4())
        self.network=network
        
    def work(self, verbose=False):
        while True:
            if not self.ordering():
                sleep(1.0) # wait due to no transactions
            if self.add_block():
                if verbose: print(self.uuid, "Added one block")
            self.network.post_chain(self.chain, self.uuid)        
            if self.resolve_conflicts():
                if verbose: print(self.uuid, "Change chain")

    def ordering(self):
        transactions=self.network.get_transactions(self.uuid)
        if len(transactions)==0:
            return False # cannot mine due to no transactions
        previous_hash=self.chain[-1].hash()
        block=Block(time(), tuple(transactions), previous_hash)
                
        if self.add_block(): 
            return True
        if self.resolve_conflicts():
            return True
                
        self.network.broadcast_block(block, self.uuid)
        return True # successfully mined

    def add_block(self):
        for block in self.network.get_blocks(self.uuid):
            # if self.verify_block(block):
                self.chain.append(block)           
                if self.verify_chain(self.chain):
                    return True
                else:
                    self.chain.pop(-1)

        return False # no block is added

    def resolve_conflicts(self):
        """Longest valid chain is authoritative"""
        # authoritative_chain=self.chain
        authoritative_chain=self.chain  
        for chain in self.network.get_neighbour_chains(self.uuid):
            if not self.verify_chain(chain):
                # node is incorrect
                continue
            if len(chain)>len(authoritative_chain):
                # Longest valid chain is authoritative
                authoritative_chain=deepcopy(chain)
        self.chain=authoritative_chain 
        # self.chain=deepcopy(self.network.get_chain('the_leader_node')) 
        return self.chain is not authoritative_chain
        
    @staticmethod
    def verify_transaction(transaction):
        if transaction.sign is None:
            return False
        h=SHA.new(transaction.str_data().encode())
        verifier=PKCS1_v1_5.new(encode_key(transaction.sender_address))
        return verifier.verify(h, binascii.unhexlify(transaction.sign))        

    def verify_block(self, block) -> bool:
        is_correct_transactions = all(map(self.verify_transaction, block.transactions))
        return is_correct_transactions
    
    def verify_chain(self, chain):
        for i in range(len(chain)-1, 0, -1):
            # if not self.verify_block(chain[i]):
            #     return False
            if chain[i-1].hash() != chain[i].previous_hash:
                return False
        return True
