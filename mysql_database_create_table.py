import sqlite3 as sql # Sqlite3 Database Connection


class DatabaseConnection(object):
    """ i). CREATE DATABASE LOGIN_APP;
        ii). CREATE TABLE LOG_DETAILS(NAME VARCHAR(20), USERNAME VARCHAR(20), PASSWORD VARCHAR(20), AVATAR VARCHAR(20));
        iii). DESC LOG_DETAILS;
    """

    def __init__(self):
        self.mydb = sql.connect('login_app.db')
        self.mycursor = self.mydb.cursor()

    def db_connection(self):
        # self.mycursor.execute("CREATE TABLE LOG_DETAILS(NAME VARCHAR(20), USERNAME VARCHAR(20), PASSWORD VARCHAR(20), AVATAR VARCHAR(20))")
        # self.mycursor.execute('''INSERT INTO LOG_DETAILS (NAME, USERNAME,PASSWORD)VALUES("Shipra","Shipra","Shipra")''')
        self.mycursor.execute('select * from LOG_DETAILS')
        result = self.mycursor.fetchall()
        for row in result:
            print(f'{row[0]:2}{row[1]}{row[2]}')
        # self.mydb.commit()
        self.mydb.close()


# Instance which gives database details
inst = DatabaseConnection()
inst.db_connection()