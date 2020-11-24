from src.database import Database
from src.config import Config


class state_getter(object):

    def __init__(self):
        """
        init
        """
        self._database = Database(Config)

    def get_state(self, user_id, time):
        res = self._database.select_rows(
            "SELECT state FROM processed_data WHERE user_id = %s ORDER BY abs(extract(epoch from (ts - timestamp %s))) LIMIT 1",
            [user_id, time])
        if res == 400:
            return "Something is not right with your request", res
        return {'user': user_id, 'time': time, 'state': res[0][0]}

    def create_user(self, username, password, email):
        res = self._database.update_rows(
            "INSERT INTO users_table (username,password,email) VALUES (%s,%s,%s) RETURNING id",
            [username, password, email])
        return res

    def insert_gsr_values(self, user_id, values, times):
        for i in range(len(values)):
            self._database.update_rows("INSERT INTO raw_data VALUES (%s,%s,%s)",
                                       [user_id, values[i], times[i]])

    def get_gsr_values(self, user_id, end_time):
        res = self._database.select_rows(
            "SELECT gsr_reading FROM raw_data WHERE user_id = %s AND ts > %s::timestamp - interval '10 seconds' AND ts < %s",
            [user_id, end_time, end_time])
        return list(map(lambda x: x[0], res))

    def insert_state(self, user_id, ts, state):
        res = self._database.update_rows("INSERT INTO processed_data VALUES (%s,%s,%s)",
                                         [user_id, ts, state])
        return res
