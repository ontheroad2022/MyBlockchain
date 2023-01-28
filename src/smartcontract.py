import json
import network
import wallet

class Smartcontract:

    def __init__(self, network):
        self.state = {"sender_address": None, "receiver_address": None, "reserved": 0}
        self.network = network

    #トランザクションの履歴を取得する
    def get_history_of_transactions_by_uuid(self, uuid):
        history = []
        for chain in json.loads(self.network.get_chain(uuid).json_dumps()):
                transactions = json.loads(chain).get('transactions')
                for t in transactions:
                    history.append(t)  

        return history             

    def get_current_state(self, uuid='the_leader_node'):
        for operand in self.get_history_of_transactions_by_uuid(uuid):
            d_operand = json.loads(operand) #convert to a dictionary
            if d_operand['value']=='reservation':
                if not self.state["reserved"]:
                    self.state["sender_address"] = d_operand["sender_address"]
                    self.state["receiver_address"] = d_operand["receiver_address"]
                    self.state["reserved"] = 1
            elif d_operand['value']=='cancel':
                if self.state["reserved"]:
                    if ((self.state["sender_address"]==d_operand["sender_address"])):
                            self.state["sender_address"] = None
                            self.state["receiver_address"] = None
                            self.state["reserved"] = 0
        return self.state

    def cancel_reservation(self, s):
        self.state = self.get_current_state('the_leader_node')
        if self.state['reserved'] and (self.state['sender_address'] == [s.address]):
            # alice.send(bob.address, 'cancel')      
            s.send([None], 'cancel')   
            s.send([None], 'cancel')
            return True
        return False

    def make_a_reservation(self, s):
        self.state = self.get_current_state('the_leader_node')
        if not self.state['reserved']:
            # alice.send(bob.address, 'reservation')     
            s.send([None], 'reservation')         
            return True
        return False