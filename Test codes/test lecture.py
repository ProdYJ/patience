import sqlite3
import os


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_last_db_value(conn, table, row, index = -1):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    command = "SELECT " + row + " FROM " + table
    cur = conn.cursor()
    cur.execute(command)

    rows = cur.fetchall()

    #for row in rows:
     #   print(row)
    if(index == -1):
        data = rows[len(rows)-1]
    elif(index<len(rows)):
        data = rows[index]
    else:
        data = "ERROR"
    
    print(data)
    return data

def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM COURANTS WHERE POMPE=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    #database = r"C:\sqlite\db\pythonsqlite.db"
    
    dir_path = os.path.dirname(os.path.realpath(__file__))      #On récupère le dossier dans lequel le code python se trouve
    database = dir_path +  '/Data.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by priority:")
        select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        get_last_db_value(conn, "DATA", "MODE", 2)


if __name__ == '__main__':
    main()