import os
from datetime import datetime
from model.stress_state import stress_states

class state_getter(object):

    def __init__(self):
        """
        init
        """

    def get_state(self, user_id, state):
        curr_state = json.loads(state)	
        return "{} is feeling {} at {}".format(user_id, curr_state['GetSensorValue'][0], curr_state['GetSensorValue'][1])

