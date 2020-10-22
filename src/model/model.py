import psycopg2
from model.stress_state import stress_states

class state_getter(object):

    def __init__(self):
        """
        init
        """
        self._conn = psycopg2.connect(dbname="scares",
                                      user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432")

    def get_state(self, user_id, state):
        curr_state = json.loads(state)	
        return "{} is feeling {} at {}".format(user_id, curr_state['GetSensorValue'][0], curr_state['GetSensorValue'][1])

    def create_user(self, username,password,email):
        cur = self._conn.cursor()
        res = cur.execute("""
                    INSERT INTO users_table (username,password,email) VALUES (%s,%s,%s)
                    RETURNING id"""
                    , (username,password,email))
        self._conn.commit()
        return res

    def insert_gsr_values(self, user_id, values, times):
        cur = self._conn.cursor()
        for i in range(len(values)):
            cur.execute("INSERT INTO raw_data VALUES (%s,%s,%s)", (user_id, values[i], times[i]))

        self._conn.commit()
