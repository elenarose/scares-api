from .stress_state import stress_states
from ..database import Database
from ..config import Config

class state_getter(object):

    def __init__(self):
        """
        init
        """
        self._database = Database(Config)

    def get_state(self, user_id, time):
        if time > 5:
            return "{} is feeling {}".format(user_id, stress_states.bad)

    def create_user(self, username,password,email):
        res = self._database.update_rows("INSERT INTO users_table (username,password,email) VALUES (%s,%s,%s) RETURNING id", [username,password,email])
        return res

    def insert_gsr_values(self, user_id, values, times):
        for i in range(len(values)):
            self._database.update_rows("INSERT INTO raw_data VALUES (%s,%s,%s)", [user_id, values[i], times[i]])

    def get_gsr_values(self, user_id, start_time, end_time):
        res = self._database.select_rows("SELECT * FROM raw_data WHERE user_id = %s AND ts > %s AND ts < %s", [user_id, start_time, end_time])
        return res