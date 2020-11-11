import psycopg2
from loguru import logger

class Database:
    """PostgreSQL Database class."""
    def __init__(self, config):
        self.host = config.PG_HOST
        self.user = config.PG_USER
        self.password = config.PG_PASSWORD
        self.port = config.PG_PORT
        self.dbname = config.PG_NAME
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(dbname=self.dbname,
                                             user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port)
            except psycopg2.DatabaseError as e:
                logger.error(e)
            finally:
                logger.info('Connection opened successfully.')

    def select_rows(self, query, params = []):
        """Run a SQL query to select rows from table."""
        self.connect()
        with self.conn.cursor() as cur:
            try:
                cur.execute(query, params)
                records = [row for row in cur.fetchall()]
                cur.close()
                return records
            except Exception as e:
                logger.error(e)
                cur.close()
                return 400

    def update_rows(self, query, params = []):
        """Run a SQL query to update rows in a table."""
        self.connect()
        with self.conn.cursor() as cur:
            try:
                res = cur.execute(query, params)
            except psycopg2.DatabaseError as e:
                logger.error(e)
                res = "Something is not right with your request", 400
            finally:
                self.conn.commit()
                cur.close()
                return res