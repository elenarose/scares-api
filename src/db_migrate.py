import psycopg2


if __name__ == '__main__':
    print("init connection")
    conn = psycopg2.connect(dbname="scares",
                            user="postgres",
                            password="postgres",
                            host="localhost",
                            port="5432")
    try:
        cur = conn.cursor()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS users_table(
                        id SERIAL NOT NULL PRIMARY KEY,
                        username VARCHAR ( 50 ) UNIQUE NOT NULL,
                        password VARCHAR ( 50 ) NOT NULL,
                        email VARCHAR ( 255 ) UNIQUE NOT NULL,
                        created_on TIMESTAMP NOT NULL
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS raw_data(
                        user_id INTEGER NOT NULL
                                REFERENCES users_table (id),
                        ts TIMESTAMP NOT NULL,
                        gsr_reading DOUBLE NOT NULL
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS processed_data(
                        user_id INTEGER NOT NULL
                                REFERENCES users_table (id),
                        ts TIMESTAMP NOT NULL,
                        state VARCHAR ( 50 ) NOT NULL
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS latest_received(
                        user_id INTEGER NOT NULL
                                REFERENCES users_table (id),
                        latest_received_ts TIMESTAMP NOT NULL
                    )
                    """)

        conn.commit()
    except:
        print("something didnt work")
    finally:
        conn.close()
    print("connection closed")