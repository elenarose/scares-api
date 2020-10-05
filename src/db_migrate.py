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

        conn.commit()
    except:
        print("something didnt work")
    finally:
        conn.close()
    print("connection closed")