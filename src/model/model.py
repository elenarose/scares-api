import os
from datetime import datetime
from model.stress_state import stress_states

class state_getter(object):

    def __init__(self):
        """
        init
        """

    def get_state(self, user_id, time):
        if time > 5:
            return "{} is feeling {}".format(user_id, stress_states.bad)

