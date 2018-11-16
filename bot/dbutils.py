# db_utils.py
import os
import sqlite3


# create a default path to connect to and create (if necessary) a database
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'emotions.sqlite3')


class DBUtils:

    def __init__(self):
        pass

    def db_connect(db_path=DEFAULT_PATH):
        con = sqlite3.connect(db_path)
        return con

    def create_emotion(conn, user_id, datetime, emotion_type):

        create_stmt = "CREATE TABLE IF NOT EXISTS \"tb_emotions_user\"" + \
                      "( `user_id` INTEGER NOT NULL, " + \
                      "`emotion_type` INTEGER NOT NULL, " + \
                      "`emotion_date_full` INTEGER NOT NULL )"

        c = conn.cursor()
        c.execute(create_stmt)
        c.execute("INSERT INTO tb_emotions_user VALUES(?, ?, ?)",
                  (user_id, emotion_type, datetime))
        conn.commit()
        c.close()
        conn.close()
        return 0

    def select_emotions_count(conn, user_id):
        try:
            cur = conn.cursor()
            cur.execute("SELECT emotion_type, count(*) " +
                        "from \"tb_emotions_user\" WHERE user_id=" +
                        user_id + " GROUP BY emotion_type")
            rows = cur.fetchall()
            return rows
        except sqlite3.OperationalError:
            return None
