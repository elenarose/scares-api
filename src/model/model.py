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

    def get_user_state(self, user_id):
        cur = self._conn.cursor()
        res = cur.execute(
            """
            SELECT user_state
            FROM user_data
            WHERE user_id = (%s) AND time = (%s)
            RETURNING user_state
            """
            , (user_id), )
        self._conn.commit()
        return res

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
